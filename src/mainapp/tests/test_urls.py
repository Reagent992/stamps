import logging
import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings

from mainapp.models import Stamp, StampGroup
from printy.models import Printy, PrintyGroup
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

logger = logging.getLogger("__name__")


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UrlsTests(TestCase):
    """
    Тест urls.py

    Оглавление:
        0. Служебное.
        1. Создание данных для тестов.
        2. Публичные страницы открываются(status = 200).
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

    def test_public_urls_stamps(self) -> None:
        """2. Страницы штампов доступные любому пользователю."""
        url_status_dict = {
            "/": HTTPStatus.OK,
            f"/{self.stamp_group1.slug}/": HTTPStatus.OK,
            f"/{self.stamp_group1.slug}/{self.stamp1.slug}/": HTTPStatus.OK,
        }
        for url, status in url_status_dict.items():
            with self.subTest(url=url, status=status):
                response = self.guest_user.get(url)
                self.assertEqual(
                    response.status_code,
                    status,
                    f"Адресу {url} не соответствует HTTP-статус {status}",
                )

    def test_public_urls_printy(self) -> None:
        """2.1 Страницы оснасток доступные любому пользователю."""
        url_status_dict = {
            "/printy/": HTTPStatus.OK,
            f"/printy/{self.printygroup1.slug}/": HTTPStatus.OK,
            f"/printy/{self.printygroup1.slug}"
            f"/{self.printy1.slug}/": HTTPStatus.OK,
        }
        for url, status in url_status_dict.items():
            with self.subTest(url=url, status=status):
                response = self.guest_user.get(url)
                self.assertEqual(
                    response.status_code,
                    status,
                    f"Адресу {url} не соответствует HTTP-статус {status}",
                )

    def test_public_urls(self) -> None:
        """2.2 Остальные публичные страницы."""
        # TODO: add flatpages
        url_status_dict = {
            "/sitemap.xml": HTTPStatus.OK,
            "/about/contacts/": HTTPStatus.OK,
        }
        for url, status in url_status_dict.items():
            with self.subTest(url=url, status=status):
                response = self.guest_user.get(url)
                self.assertEqual(
                    response.status_code,
                    status,
                    f"Адресу {url} не соответствует HTTP-статус {status}",
                )
