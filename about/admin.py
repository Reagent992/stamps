from django.contrib import admin

from about.models import (ContactPhone, ContactEmail, ContactSocial,
                          ContactMessage, ContactYandexMap, ContactAddress,
                          ContactTelegram)

admin.site.register(ContactPhone)
admin.site.register(ContactEmail)
admin.site.register(ContactSocial)
admin.site.register(ContactMessage)
admin.site.register(ContactYandexMap)
admin.site.register(ContactAddress)
admin.site.register(ContactTelegram)
