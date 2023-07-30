from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class UrlsTests(TestCase):
    def setUp(self) -> None:
        """Создаем данные для тестирования"""
        super().setUp()
        # Создаем неавторизованного пользователя
        self.guest_client = Client()

    def test_urls_guest(self):
        """Страницы доступные любому пользователю"""
        url_status_dict = {
            '/': HTTPStatus.OK,
        }
        for url, status in url_status_dict.items():
            with self.subTest(url=url, status=status):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)
