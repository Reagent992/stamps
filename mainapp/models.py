from django.db import models
from django.urls import reverse

from core.abstract_models import AbstractItemModel, AbstrcatGroupModel
from printy.models import Printy


class StampGroup(AbstrcatGroupModel):
    """Группы печатей."""

    pic_upload_place = "group_pics/"

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

    pic_upload_place = "stamps/"

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
            "Печать должна быть привязанна хотя бы к одной оснастке."
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
