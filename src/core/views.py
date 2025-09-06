from django.conf import settings
from django.http.request import HttpRequest
from django.shortcuts import render


def permission_denied(request: HttpRequest, _):
    """Custom template for 403(Forbiden) error."""
    return render(request, settings.ERROR_403_TEMPLATE, status=403)


def page_not_found(request: HttpRequest, _):
    """Page for 404(Not Found) error."""
    return render(
        request,
        settings.ERROR_404_TEMPLATE,
        {"title": settings.ERROR_404_TITLE},
        status=404,
    )
