import shutil
import tempfile
from typing import Optional
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from mainapp.models import Stamp, StampGroup
from orders.models import Order
from printy.models import Printy, PrintyGroup
from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class SeleniumMainAppTestCase(LiveServerTestCase):
    """
    Functional tests with Selenium.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # -------------------------------------------------------------Selenium
        cls.options = webdriver.ChromeOptions()
        cls.options.add_argument("--headless")
        cls.options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=cls.options)
        cls.driver.get(cls.live_server_url)
        cls.wait = WebDriverWait(cls.driver, 2, 0.1)
        # -------------------------------------------------------------Fixtures
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
        cls.stamp1.printy.add(cls.printy1)
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
        # ----------------------------------------------------------------Order
        cls.field1_fill = "field1_fill"
        cls.field2_fill = "field2_fill"
        cls.email = "test@example.com"
        cls.phone = "+7 912 345 67 89"
        cls.name = "Иван"
        cls.address = "ул. Пушкина, д. 2"
        cls.city = "Москва"
        cls.postal_code = "123456"
        cls.comment = "Пример комментария для тестирования формы"

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cls.driver.quit()

    def setUp(self) -> None:
        super().setUp()
        self.driver.refresh()

    def find_element(self, element_type: str, query: str) -> WebElement:
        return self.wait.until(
            EC.visibility_of_element_located(
                (
                    element_type,
                    query,
                )
            ),
            f"Timed out while looking for: <{element_type=}> <{query=}>",
        )

    def find_elements(self, element_type: str, query: str) -> list[WebElement]:
        return self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    element_type,
                    query,
                )
            ),
            f"Timed out while looking for: <{element_type=}> <{query=}>",
        )

    def get_cards(self) -> list[WebElement]:
        return self.find_elements(By.CLASS_NAME, "card")

    def click_button(self, element: Optional[WebElement] = False) -> None:
        if element:
            return element.find_element(By.CLASS_NAME, "btn").click()
        return self.find_element(By.CLASS_NAME, "btn").click()

    @patch("orders.tasks.send_order_email.delay")
    def test_create_order(self, send_order_email: MagicMock) -> None:
        """Goes through the order process: choose stamp,
        printy, fill in information, check if email was sent."""
        group_cards = self.get_cards()
        self.assertTrue(len(group_cards) == settings.PAGINATION_AMOUNT)
        self.click_button(group_cards[0])
        pagination_element = self.find_element(By.CLASS_NAME, "pagination")
        page_buttons = pagination_element.find_elements(
            By.CLASS_NAME, "page-item"
        )
        page_buttons[-1].click()
        stamps_cards = self.find_elements(By.CLASS_NAME, "card")
        self.click_button(stamps_cards[-1])
        self.click_button()
        printy_group_cards = self.get_cards()
        self.assertTrue(len(printy_group_cards), 1)
        self.click_button(printy_group_cards[0])
        printy_cards = self.get_cards()
        self.assertTrue(len(printy_cards), 1)
        self.click_button(printy_cards[0])
        self.click_button()
        self.find_element(By.ID, f"id_{self.stamp_field1}").send_keys(
            self.field1_fill
        )
        self.find_element(By.ID, f"id_{self.stamp_field2}").send_keys(
            self.field2_fill
        )
        self.find_element(By.ID, "id_email").send_keys(self.email)
        self.find_element(By.ID, "id_phone").send_keys(self.phone)
        self.find_element(By.ID, "id_name").send_keys(self.name)
        self.find_element(By.ID, "id_address").send_keys(self.address)
        self.find_element(By.ID, "id_city").send_keys(self.city)
        self.find_element(By.ID, "id_postal_code").send_keys(self.postal_code)
        self.find_element(By.ID, "id_comment").send_keys(self.comment)
        self.find_element(By.CLASS_NAME, "btn").submit()
        send_order_email.assert_called_once()

        order = Order.objects.first()
        self.assertTrue(order.email, self.email)
        self.assertTrue(order.phone, self.phone)
        self.assertTrue(order.name, self.name)
        self.assertTrue(order.address, self.address)
        self.assertTrue(order.city, self.city)
        self.assertTrue(order.postal_code, self.postal_code)
        self.assertTrue(order.comment, self.comment)
        self.assertTrue(
            order.stamp_text,
            {
                self.stamp_field1: self.field1_fill,
                self.stamp_field2: self.field2_fill,
            },
        )
