import logging
import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from mainapp.models import Stamp, StampGroup
from printy.models import Printy, PrintyGroup
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

logger = logging.getLogger("__name__")


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class StampTests(TestCase):
    """
    View Штампов и Оснасток тестируются вместе.

    Оглавление:
    0. Служебное.
    1. Создание данных для тестов.
    2. View use the expected HTML templates.
    3. Выбраны правильные заголовки для страниц.
    4. Context of view contains necessary objects.
    5. Pagination
    """

    @classmethod
    def tearDownClass(cls) -> None:
        """0. Удаляем временную папку для медиа-файлов."""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpClass(cls) -> None:
        """1. Создаем данные для тестов."""
        super().setUpClass()
        # Анонимный пользователь.
        cls.guest_user = Client()
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
        # pagination
        obj_array = [
            StampGroup(
                title=f"Тестовая группа штампов {i}",
                slug=f"test_group{i}",
                image=cls.uploaded,
                published=True,
            )
            for i in range(2, 16)
        ]
        StampGroup.objects.bulk_create(obj_array)
        obj_array = [
            PrintyGroup(
                title=f"Тестовая группа оснасток {i}",
                slug=f"test_printy_group{i}",
                image=cls.uploaded,
                published=True,
            )
            for i in range(2, 16)
        ]
        PrintyGroup.objects.bulk_create(obj_array)
        for i in range(2, 16):
            cur_obj = Stamp(
                title=f"Тестовый штамп {i}",
                slug=f"test_stamp{i}",
                description="Описание тестового штампа",
                price=399,
                published=True,
                image=cls.uploaded,
                group=cls.stamp_group1,
                form_fields=cls.stamp_fields_group,
            )
            cur_obj._skip_celery_task = True
            cur_obj.save(force_insert=True)
        for i in range(2, 16):
            cur_obj = Printy(
                title=f"Тестовая оснастка {i}",
                slug=f"test_printy{i}",
                description="Описание тестовой оснастки",
                price=299,
                published=True,
                image=cls.uploaded,
                group=cls.printygroup1,
            )
            cur_obj._skip_celery_task = True
            cur_obj.save(force_insert=True)
        cls.first_stamp = Stamp.objects.first()
        cls.first_printy = Printy.objects.first()
        # pagination test expect it to be equal
        cls.objects_amount = 15
        assert Stamp.objects.count() == cls.objects_amount
        assert Printy.objects.count() == cls.objects_amount
        assert StampGroup.objects.count() == cls.objects_amount
        assert PrintyGroup.objects.count() == cls.objects_amount

    def test_pages_use_correct_template_stamps(self) -> None:
        """2. View use the expected HTML templates."""
        stamps_templates = {
            reverse("mainapp:index"): settings.INDEX_TEMPLATE,
            reverse(
                "mainapp:stamps", kwargs={"group": self.stamp_group1.slug}
            ): settings.INDEX_TEMPLATE,
            reverse(
                "mainapp:item_details",
                kwargs={
                    "group": self.stamp1.group.slug,
                    "slug_item": self.stamp1.slug,
                },
            ): settings.ITEM_DETAIL_TEMPLATE,
            reverse("printy:printy_index"): settings.INDEX_TEMPLATE,
            reverse(
                "printy:printys",
                kwargs={"printy_group": self.printygroup1.slug},
            ): settings.INDEX_TEMPLATE,
            reverse(
                "printy:printy_details",
                kwargs={
                    "printy_group": self.printy1.group.slug,
                    "printy_item": self.printy1.slug,
                },
            ): settings.ITEM_DETAIL_TEMPLATE,
        }
        for reverse_name, template in stamps_templates.items():
            with self.subTest(reverse_name=reverse_name, template=template):
                response = self.guest_user.get(reverse_name)
                self.assertTemplateUsed(
                    response,
                    template,
                    f"На странице {reverse_name} "
                    f"не использован требуемый шаблон: {template}",
                )

    def test_pages_use_correct_titles_stamps(self) -> None:
        """3. Выбраны правильные заголовки для страниц."""
        titles_pages = {
            reverse("mainapp:index"): settings.INDEX_TITLE,
            reverse(
                "mainapp:stamps", kwargs={"group": self.stamp_group1.slug}
            ): self.stamp_group1.title,
            reverse(
                "mainapp:item_details",
                kwargs={
                    "group": self.stamp_group1.slug,
                    "slug_item": self.stamp1.slug,
                },
            ): self.stamp1.title,
            reverse("printy:printy_index"): settings.PRINTY_TITLE,
            reverse(
                "printy:printys",
                kwargs={"printy_group": self.printygroup1.slug},
            ): self.printygroup1.title,
            reverse(
                "printy:printy_details",
                kwargs={
                    "printy_group": self.printy1.group.slug,
                    "printy_item": self.printy1.slug,
                },
            ): self.printy1.title,
        }
        for page, title in titles_pages.items():
            with self.subTest(page=page, title=title):
                response = self.guest_user.get(page)
                self.assertEqual(
                    response.context.get("title"),
                    title,
                    "Не совпадают заголовки вкладки.",
                )

    def test_view_stamps_context_contain_object(self) -> None:
        """4. Context of view contains necessary objects."""
        pages = (
            (reverse("mainapp:index"), self.stamp_group1, True),
            (
                reverse(
                    "mainapp:stamps",
                    kwargs={"group": self.first_stamp.group.slug},
                ),
                self.first_stamp,
                False,
            ),
            (
                reverse(
                    "mainapp:item_details",
                    kwargs={
                        "group": self.first_stamp.group.slug,
                        "slug_item": self.first_stamp.slug,
                    },
                ),
                self.first_stamp,
                False,
            ),
            (reverse("printy:printy_index"), self.printygroup1, True),
            (
                reverse(
                    "printy:printys",
                    kwargs={"printy_group": self.first_printy.group.slug},
                ),
                self.first_printy,
                False,
            ),
            (
                reverse(
                    "printy:printy_details",
                    kwargs={
                        "printy_group": self.first_printy.group.slug,
                        "printy_item": self.first_printy.slug,
                    },
                ),
                self.first_printy,
                False,
            ),
        )
        for path, test_obj, its_group in pages:
            with self.subTest(path=path, test_obj=test_obj):
                response = self.guest_user.get(path)
                response_obj = response.context.get("page_obj")
                if response_obj:
                    response_obj = response_obj[0]
                else:
                    response_obj = response.context.get("object")
                self.assert_attributes_equal(
                    response_obj, test_obj, path, its_group
                )

    def assert_attributes_equal(
        self, response_obj, test_obj, path, its_group=False
    ) -> None:
        """Assert equality of attributes between response_obj and test_obj."""
        attributes = [
            "title",
            "slug",
            "description",
            "price",
            "published",
            "image",
            "group",
        ]
        if its_group:
            attributes = ["title", "slug", "image", "published"]
        for attribute in attributes:
            response_attr = getattr(response_obj, attribute)
            test_obj_attr = getattr(test_obj, attribute)
            self.assertEqual(
                response_attr,
                test_obj_attr,
                f"ojb {response_obj} from {path}"
                f" don't have {attribute}={test_obj_attr}",
            )

    def calculate_last_page_number(self) -> int:
        t = self.objects_amount // settings.PAGINATION_AMOUNT
        if self.objects_amount % settings.PAGINATION_AMOUNT:
            return t + 1
        return t

    def calculate_amount_of_items_on_last_page(self) -> int:
        if not self.objects_amount % settings.PAGINATION_AMOUNT:
            return self.objects_amount // settings.PAGINATION_AMOUNT
        return self.objects_amount % settings.PAGINATION_AMOUNT

    def test_pagination(self) -> None:
        urls = (
            reverse("mainapp:index"),
            reverse(
                "mainapp:stamps",
                kwargs={"group": self.stamp_group1.slug},
            ),
            reverse("printy:printy_index"),
            reverse(
                "printy:printys",
                kwargs={"printy_group": self.printygroup1.slug},
            ),
        )
        for url in urls:
            with self.subTest(url=url):
                first_page = self.client.get(url)
                last_page = self.client.get(
                    url + f"?page={self.calculate_last_page_number()}"
                )
                self.assertEqual(
                    len(first_page.context["page_obj"]),
                    settings.PAGINATION_AMOUNT,
                    "Incorrect number of objects on the first page.",
                )
                self.assertEqual(
                    len(last_page.context["page_obj"]),
                    self.calculate_amount_of_items_on_last_page(),
                    "Incorrect number of objects on the last page.",
                )
                self.assertNotContains(
                    first_page,
                    last_page.context["page_obj"],
                    HTTPStatus.OK,
                    msg_prefix=(
                        "First_page should not contain last_page objects."
                    ),
                )
