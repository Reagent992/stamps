from django.db import models

from core.abstract_models import AbstractTimeModel


class FieldsTypes(AbstractTimeModel):
    """Типы полей необходимых для заполнения при покупке штампа."""

    name = models.CharField(
        max_length=50,
        verbose_name="Поле",
    )
    re = models.CharField(
        max_length=100,
        blank=True,
        help_text="Дополнительная валидация через регулярное выражение",
        verbose_name="Регулярное выражение",
    )
    help_text = models.CharField(
        max_length=150, verbose_name="Подпись под полем"
    )

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Поля печати"
        verbose_name_plural = "Поля печати"

    def __str__(self):
        return self.name


class GroupOfFieldsTypes(AbstractTimeModel):
    """Группа типов полей."""

    name = models.CharField(max_length=100, verbose_name="Название группы")
    fields = models.ManyToManyField(
        to=FieldsTypes,
        verbose_name="Поля",
    )

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Группа полей печати"
        verbose_name_plural = "Группы полей печати"

    def __str__(self):
        return self.name
