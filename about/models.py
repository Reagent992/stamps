from django.db import models


class ContactPhone(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=16)
    published = models.BooleanField()

    def __str__(self):
        return self.phone


class ContactEmail(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    published = models.BooleanField()

    def __str__(self):
        return self.email


class ContactSocial(models.Model):
    name = models.CharField(max_length=200)
    vk = models.URLField()
    double_gis = models.URLField()
    published = models.BooleanField()

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Viber, What Up link."""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=16)
    published = models.BooleanField()

    def __str__(self):
        return self.phone


class ContactTelegram(models.Model):
    """Текстовая часть ссылки на Telegram."""
    name = models.CharField(max_length=200)
    tg_name = models.CharField(max_length=30)
    published = models.BooleanField()

    def __str__(self):
        return self.tg_name


class ContactYandexMap(models.Model):
    name = models.CharField(max_length=200)
    map = models.TextField()
    published = models.BooleanField()

    def __str__(self):
        return self.name


class ContactAddress(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    published = models.BooleanField()

    def __str__(self):
        return self.address
