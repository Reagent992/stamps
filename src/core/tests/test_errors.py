import logging
from http import HTTPStatus
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.test import Client, TestCase, override_settings
from django.urls import include, path, reverse

from config.urls import handler403, handler404, handler500


# fixtures
def view_403(_: HttpRequest):
    raise PermissionDenied


def view_500(_: HttpRequest):
    raise Exception


PATH_403 = uuid4().hex
PATH_500 = uuid4().hex
handler500, handler404, handler403 = handler500, handler404, handler403
urlpatterns = [
    path(PATH_403, view_403, name=PATH_403),
    path(PATH_500, view_500, name=PATH_500),
    path("", include("config.urls")),
]


@override_settings(ROOT_URLCONF=__name__)
class TestErrors(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.guest_user = Client(raise_request_exception=False)
        # Disable logging due to both tests write expected errors.
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        logging.disable(logging.NOTSET)

    def test_404_error(self) -> None:
        response = self.guest_user.get(f"{uuid4().hex}/")
        self.assertTemplateUsed(response, settings.ERROR_404_TEMPLATE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_403_error(self) -> None:
        response = self.guest_user.get(
            reverse(
                PATH_403,
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertTemplateUsed(response, settings.ERROR_403_TEMPLATE)

    def test_500_error(self) -> None:
        response = self.guest_user.get(
            reverse(
                PATH_500,
            )
        )
        self.assertEqual(
            response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR
        )
        self.assertTemplateUsed(response, settings.ERROR_500_TEMPLATE)
