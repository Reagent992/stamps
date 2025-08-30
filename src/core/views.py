from django.conf import settings
from django.shortcuts import render


def page_not_found(request, exception):
    """Custom 404 error handler that renders our custom 404 template."""
    return render(request, settings.ERROR_404_TEMPLATE, status=404)
