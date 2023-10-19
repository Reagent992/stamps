from django.utils import timezone


def year(request):
    """Add current year variable to Template."""
    current_year = timezone.now().year
    return {"year": current_year}
