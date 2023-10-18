from django.db import models

from core.abstract_models import AbstractItemModel, AbstrcatGroupModel
from printy.models import Printy


class StampGroup(AbstrcatGroupModel):
    """Группы печатей."""

    pic_upload_place = "group_pics/"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Группа печатей"
        verbose_name_plural = "Группы печатей"

    def __str__(self):
        return self.title


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
        to=Printy, blank=True, related_name="printy", verbose_name="Оснастка"
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Печать"
        verbose_name_plural = "Печати"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "group"], name="unique_title_group"
            )
        ]

    def __str__(self):
        return self.title
