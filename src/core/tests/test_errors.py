import logging
from http import HTTPStatus
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import path, reverse

from config.urls import urlpatterns


def view_403(_: HttpRequest):
    raise PermissionDenied


"""
Since Django caches ROOT_URLCONF,
we need to explicitly provide the temporary
urlpatterns to `reverse()`.
"""

PATHNAME_403 = "test_403"
urlpatterns.insert(0, path(uuid4().hex, view_403, name=PATHNAME_403))


class TestErrors(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.guest_user = Client()

    def setUp(self):
        # Disable logging due to both tests write expected errors.
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_404_error(self) -> None:
        response = self.guest_user.get(f"{uuid4().hex}/")
        self.assertTemplateUsed(response, settings.ERROR_404_TEMPLATE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_403_error(self) -> None:
        print(__name__)
        response = self.guest_user.get(
            reverse(
                PATHNAME_403,
                __name__,
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTemplateUsed(response, settings.ERROR_403_TEMPLATE)
