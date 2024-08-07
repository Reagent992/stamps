from django.db import models
from django.urls import reverse

from core.abstract_models import AbstractGroupModel, AbstractItemModel


class PrintyGroup(AbstractGroupModel):
    """Группы оснасток для печатей."""

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Группа оснасток"
        verbose_name_plural = "Группы оснасток"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает абсолютный URL для объекта модели."""
        return reverse(
            "printy:printys",
            kwargs={"printy_group": self.slug},
        )


class Printy(AbstractItemModel):
    """Оснастка."""

    group = models.ForeignKey(
        to=PrintyGroup,
        on_delete=models.RESTRICT,
        related_name="printy",
        verbose_name="Группа оснасток",
        help_text="Группа, к которой будет относиться оснастка",
    )

    class Meta:
        ordering = ("-updated",)
        verbose_name = "Оснастка"
        verbose_name_plural = "Оснастки"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "group"], name="unique_printy_title_group"
            )
        ]

    def __str__(self):
        return f"{self.title} | {self.group.title}"

    def get_absolute_url(self):
        """Возвращает абсолютный URL для объекта модели."""
        return reverse(
            "printy:printy_details",
            kwargs={"printy_item": self.slug, "printy_group": self.group.slug},
        )
