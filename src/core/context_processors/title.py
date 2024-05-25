from django.conf import settings


def title(request):
    """Add end of title variable to Template."""
    return {"extend_title": settings.TITLE}
