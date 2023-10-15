from django.conf import settings
from django.views.generic import TemplateView

from about.models import Contact, ContactYandexMap
from core.mixins import PageTitleViewMixin


class ContactView(PageTitleViewMixin, TemplateView):
    """Страница контактов."""

    template_name = "about/contacts.html"
    title = settings.ABOUT_CONTACTS_TITLE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "map_list": ContactYandexMap.objects.filter(published=True),
                "contact": Contact.objects.filter(published=True),
            }
        )
        return context
