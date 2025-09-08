from django.conf import settings
from django.http.request import HttpRequest
from django.shortcuts import render


def permission_denied(request: HttpRequest, exception):
    """Custom template for 403(Forbiden) error."""
    return render(
        request,
        settings.ERROR_403_TEMPLATE,
        {"title": settings.ERROR_403_TITLE},
        status=403,
    )


def page_not_found(request: HttpRequest, exception):
    """Page for 404(Not Found) error."""
    return render(
        request,
        settings.ERROR_404_TEMPLATE,
        {"title": settings.ERROR_404_TITLE},
        status=404,
    )


def server_error(request: HttpRequest, exception):
    """Custom template for 500(Internal Server Error) error."""
    return render(
        request,
        settings.ERROR_500_TEMPLATE,
        {"title": settings.ERROR_500_TITLE},
        status=500,
    )
