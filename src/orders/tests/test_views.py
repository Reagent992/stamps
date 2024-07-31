import shutil
import tempfile
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from mainapp.factory import StampFactory, StampGroupFactory
from orders.models import Order
from printy.factory import PrintyFactory, PrintyGroupFactory
from stamp_fields.factory import FieldsTypesFactory, GroupOfFieldsTypesFactory

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestCaseOrder(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        """0. Удаляем временную папку для медиа-файлов."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    @patch("core.tasks.paste_watermark_and_resize_image.delay")
    def setUpClass(cls, mocked_task: MagicMock) -> None:
        """1. Создаем данные для тестов."""
        super().setUpClass()
        # ------------------------------------------------------------Constants
        cls.AMOUNT_OF_GROUPS = 15
        # -------------------------------------------------------------Fixtures
        # Группа оснасток.
        cls.printygroup1 = PrintyGroupFactory.create()
        # Оснастка.
        cls.printy1 = PrintyFactory.create(group=cls.printygroup1)
        # Поля для печати.
        cls.stamp_field1 = FieldsTypesFactory.create()
        cls.stamp_field2 = FieldsTypesFactory.create()
        # Группа полей печати.
        cls.stamp_field_fields = GroupOfFieldsTypesFactory.create(
            fields=[cls.stamp_field1, cls.stamp_field2]
        )
        # Группа штампов.
        cls.stamp_group1 = StampGroupFactory.create()
        # Штамп.
        cls.stamp1 = StampFactory.create(
            group=cls.stamp_group1,
            form_fields=cls.stamp_field_fields,
            printy=[cls.printy1],
        )
        # Objects for pagination.
        [
            PrintyFactory.create(group=cls.printygroup1)
            for _ in range(cls.AMOUNT_OF_GROUPS - 1)
        ]
        StampGroupFactory.create_batch(cls.AMOUNT_OF_GROUPS - 1)
        # Анонимный пользователь.
        cls.guest_user = Client()
        # Select printy and stamp.
        session = cls.guest_user.session
        session[settings.USER_CHOICE_PRINTY_ID] = cls.printy1.id
        session[settings.USER_CHOICE_STAMP_ID] = cls.stamp1.id
        session.save()

    @patch("orders.tasks.send_telegram_message.delay_on_commit")
    @patch("orders.tasks.send_order_email.delay_on_commit")
    def test_new_order_creation(
        self, send_order_email: MagicMock, send_telegram_message: MagicMock
    ) -> None:
        """
        - Create new order.
        - Check that order was created.
        - Check that email func was called.
        - Check that telegram func was called.
        - Redirect to success page.
        """
        orders_before_new_order = Order.objects.count()
        form_data = {
            self.stamp_field1.name: "text1",
            self.stamp_field2.name: "text2",
            "email": "test@test.com",
            "phone": "1234567890",
            "name": "test_name",
            "address": "Test address",
            "city": "Test_city",
            "postal_code": "123456",
            "comment": "Test comment",
        }
        response = self.guest_user.post(
            reverse("orders:create_order"),
            data=form_data,
            follow=True,
        )
        order = Order.objects.last()
        self.assertEqual(Order.objects.count(), orders_before_new_order + 1)
        send_order_email.assert_called_once_with(order.id, order.email)
        send_telegram_message.assert_called_once()
        self.assertRedirects(response, reverse("orders:order_success"))
