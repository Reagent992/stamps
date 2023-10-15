from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Contact(models.Model):
    contacts = CKEditor5Field("Контакты", config_name="extends")
    links = CKEditor5Field("Ссылки", config_name="extends")
    published = models.BooleanField(
        verbose_name="Опубликованно",
        help_text="Включение и выключение отображения на сайте",
    )

    class Meta:
        verbose_name_plural = "Контакты"

    def __str__(self) -> str:
        return 'Редактирование страницы "Контакты"'


class ContactYandexMap(models.Model):
    name = models.CharField(max_length=200)
    map = models.TextField()
    published = models.BooleanField()

    def __str__(self):
        return self.name
