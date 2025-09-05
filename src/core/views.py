from django.conf import settings
from django.http.request import HttpRequest
from django.shortcuts import render


def permission_denied(request: HttpRequest, _):
    """Custom template for 403(Forbiden) error."""
    return render(request, settings.ERROR_403_TEMPLATE, status=403)


def page_not_found(request: HttpRequest, _):
    """Custom 404 error handler that renders our custom 404 template."""
    return render(
        request,
        settings.ERROR_404_TEMPLATE,
        {"title": settings.ERROR_404_TITLE},
        status=404,
    )
