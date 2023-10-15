from ckeditor.fields import RichTextField
from django.db import models


class Contact(models.Model):
    contants = RichTextField(verbose_name="Контакты")
    links = RichTextField(verbose_name="Ссылки")

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
