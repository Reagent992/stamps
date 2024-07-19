import logging
import shutil
import tempfile
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from mainapp.models import Stamp, StampGroup
from orders.models import Order
from printy.models import Printy, PrintyGroup
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
logger = logging.getLogger("__name__")


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestCaseOrder(TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        """0. Удаляем временную папку для медиа-файлов."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpClass(cls) -> None:
        """1. Создаем данные для тестов."""
        super().setUpClass()
        # Создаем картинки.
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00"
            b"\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        cls.uploaded = SimpleUploadedFile(
            name="small.gif", content=cls.small_gif, content_type="image/gif"
        )
        # Группа оснасток.
        cls.printygroup1 = PrintyGroup.objects.create(
            title="Тестовая группа оснасток",
            slug="test_printy_group1",
            image=cls.uploaded,
            published=True,
        )
        # Оснастка.
        cls.printy1 = Printy(
            title="Тестовая оснастка",
            slug="test_printy1",
            description="Описание тестовой оснастки",
            price=299,
            published=True,
            image=cls.uploaded,
            group=cls.printygroup1,
        )
        cls.printy1._skip_celery_task = True
        cls.printy1.save(force_insert=True)
        # Поля для печати.
        cls.stamp_field1 = FieldsTypes.objects.create(
            name="Тестовое поле для печати",
            re="",
            help_text="Тестовое поле для печати",
        )
        cls.stamp_field2 = FieldsTypes.objects.create(
            name="Тестовое поле для печати2",
            re="",
            help_text="Тестовое поле для печати2",
        )
        # Группа полей для печати.
        cls.stamp_fields_group = GroupOfFieldsTypes.objects.create(
            name="Тестовая группа полей для печати"
        )
        cls.stamp_fields_group.fields.add(cls.stamp_field1, cls.stamp_field2)
        # Группа штампов.
        cls.stamp_group1 = StampGroup.objects.create(
            title="Тестовая группа",
            slug="test_group",
            image=cls.uploaded,
            published=True,
        )
        # Штамп.
        cls.stamp1 = Stamp(
            title="Тестовый штамп",
            slug="test_stamp1",
            description="Описание тестового штампа",
            price=399,
            published=True,
            image=cls.uploaded,
            group=cls.stamp_group1,
            form_fields=cls.stamp_fields_group,
        )
        cls.stamp1._skip_celery_task = True
        cls.stamp1.save(force_insert=True)
        # Анонимный пользователь.
        cls.guest_user = Client()
        # Select printy and stamp.
        session = cls.guest_user.session
        session[settings.USER_CHOICE_PRINTY_ID] = cls.printy1.id
        session[settings.USER_CHOICE_STAMP_ID] = cls.stamp1.id
        session.save()

    @patch("orders.tasks.send_order_email.delay")
    def test_create_of_new_order(self, send_order_email: MagicMock) -> None:
        """
        - Create new order.
        - Check that order was created.
        - Check that email func was called.
        - Redirect to success page.
        """
        orders_count = Order.objects.count()
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
        self.assertEqual(Order.objects.count(), orders_count + 1)
        send_order_email.assert_called_once_with(
            (Order.objects.last().id, Order.objects.last().email),
            countdown=settings.TASK_BEGIN_DELAY,
        )
        self.assertRedirects(response, reverse("orders:order_success"))
