from django.conf import settings
from django.views.generic import TemplateView

from about.models import (ContactEmail, ContactMessage, ContactPhone,
                          ContactSocial, ContactTelegram, ContactYandexMap)
from core.mixins import PageTitleViewMixin


class Contacts(PageTitleViewMixin, TemplateView):
    """Страница контактов."""

    template_name = 'about/contacts.html'
    title = settings.ABOUT_CONTACTS_TITLE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'phone_list': ContactPhone.objects.filter(published=True),
            'email_list': ContactEmail.objects.filter(published=True),
            'map_list': ContactYandexMap.objects.filter(published=True),
            'social_link_list': ContactSocial.objects.filter(published=True),
            'message_list': ContactMessage.objects.filter(published=True),
            'telegram': ContactTelegram.objects.filter(published=True)
        })
        return context
