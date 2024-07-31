import shutil
import tempfile
from typing import Optional
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.selenium_utils import Scrolls
from mainapp.factory import StampFactory, StampGroupFactory
from orders.models import Order
from printy.factory import PrintyFactory, PrintyGroupFactory
from stamp_fields.factory import FieldsTypesFactory, GroupOfFieldsTypesFactory

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class SeleniumMainAppTestCase(LiveServerTestCase):
    """
    Functional tests with Selenium.
    """

    @classmethod
    @patch("core.tasks.paste_watermark_and_resize_image.delay")
    def setUpClass(cls, mocked_task) -> None:
        super().setUpClass()
        # -------------------------------------------------------------Selenium
        cls.options = webdriver.ChromeOptions()
        cls.options.add_argument("--headless")
        cls.options.add_argument("--window-size=1920,1080")
        cls.driver = webdriver.Chrome(options=cls.options)
        cls.driver.get(cls.live_server_url)
        cls.wait = WebDriverWait(cls.driver, 2, 0.1)
        cls.action = webdriver.ActionChains(cls.driver)
        cls.utils = Scrolls(cls.driver, cls.action)
        # ------------------------------------------------------------Constants
        cls.AMOUNT_OF_GROUPS = 15
        # -------------------------------------------------------------Fixtures
        # Группа оснасток.
        cls.printygroup1 = PrintyGroupFactory.create()
        # Оснастка.
        cls.printy1 = PrintyFactory.create()
        # Поля для печати.
        cls.stamp_field1 = FieldsTypesFactory.create()
        cls.stamp_field2 = FieldsTypesFactory.create()
        # Группа полей печати.
        cls.stamp_field_fields = GroupOfFieldsTypesFactory.create()
        # Группа штампов.
        cls.stamp_group1 = StampGroupFactory.create()
        # Штамп.
        cls.stamp1 = StampFactory.create()
        # Objects for pagination.
        PrintyFactory.create_batch(cls.AMOUNT_OF_GROUPS - 1)
        StampGroupFactory.create_batch(cls.AMOUNT_OF_GROUPS - 1)
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
            EC.visibility_of_element_located((element_type, query)),
            f"Timed out while looking for: <{element_type=}> <{query=}>",
        )

    def find_elements(self, element_type: str, query: str) -> list[WebElement]:
        return self.wait.until(
            EC.presence_of_all_elements_located((element_type, query)),
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
        # Select stamp group.
        self.utils.scroll_to_bottom_with_sleep()
        stamp_group_cards = self.get_cards()
        self.assertEqual(len(stamp_group_cards), self.AMOUNT_OF_GROUPS)
        stamp_group = stamp_group_cards[-1]
        self.utils.scroll_to_element(stamp_group)
        stamp_group_title = stamp_group.find_element(
            By.CLASS_NAME, "fw-bolder"
        )
        self.assertEqual(stamp_group_title.text, self.stamp_group1.title)
        self.click_button(stamp_group)

        # Select stamp.
        self.utils.scroll_to_bottom_with_sleep()
        last_stamp = self.get_cards()[-1]
        self.click_button(last_stamp)
        self.click_button()
        printy_group_cards = self.get_cards()
        self.assertTrue(len(printy_group_cards), 1)
        self.click_button(printy_group_cards[0])
        printy_cards = self.get_cards()
        self.assertTrue(len(printy_cards), 1)
        self.click_button(printy_cards[0])
        self.click_button()

        # Fill order.
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

        # Check order.
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
