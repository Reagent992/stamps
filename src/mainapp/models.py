from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.abstract_models import AbstractGroupModel, AbstractItemModel
from printy.models import Printy
from stamp_fields.models import GroupOfFieldsTypes

User = get_user_model()


class StampGroup(AbstractGroupModel):
    """Группы печатей."""

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Группа печатей"
        verbose_name_plural = "Группы печатей"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает абсолютный URL для объекта модели."""
        return reverse(
            "mainapp:stamps",
            kwargs={"group": self.slug},
        )


class Stamp(AbstractItemModel):
    """Печать."""

    form_fields = models.ForeignKey(
        to=GroupOfFieldsTypes,
        on_delete=models.RESTRICT,
        verbose_name="Набор полей",
        related_name="stamps",
    )
    group = models.ForeignKey(
        to=StampGroup,
        on_delete=models.RESTRICT,
        related_name="stamps",
        verbose_name="Группа",
    )
    printy = models.ManyToManyField(
        to=Printy,
        related_name="printy",
        verbose_name="Оснастка",
        help_text="Оснастки доступные для этой печати",
        blank=False,
        error_messages=(
            "Печать должна быть привязана хотя бы к одной оснастке."
        ),
    )

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Печать"
        verbose_name_plural = "Печати"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "group"], name="unique_title_group"
            )
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает абсолютный URL для объекта модели."""
        return reverse(
            "mainapp:item_details",
            kwargs={"slug_item": self.slug, "group": self.group.slug},
        )
