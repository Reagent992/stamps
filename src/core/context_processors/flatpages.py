from django.contrib.flatpages.models import FlatPage


def flatpages(request):
    """Add public flatpages queryset to context."""
    flatpages_queryset = FlatPage.objects.filter(registration_required=False)
    return {"flatpages_queryset": flatpages_queryset}
