from django.shortcuts import render
from django.views.decorators.cache import cache_page

from about.models import ContactPhone, ContactEmail, ContactYandexMap, \
    ContactSocial, ContactMessage, ContactTelegram


@cache_page(60 * 60)
def contacts(request):
    template = 'about/contacts.html'

    contact_phones = ContactPhone.objects.filter(published=True)
    contact_emails = ContactEmail.objects.filter(published=True)
    contact_map = ContactYandexMap.objects.filter(published=True)
    contact_links = ContactSocial.objects.filter(published=True)
    contact_message = ContactMessage.objects.filter(published=True)
    telegram = ContactTelegram.objects.filter(published=True)

    context = {
        'title': 'Контакты',
        'phone_list': contact_phones,
        'email_list': contact_emails,
        'map_list': contact_map,
        'social_link_list': contact_links,
        'message_list': contact_message,
        'telegram': telegram
    }
    return render(request, template, context)
