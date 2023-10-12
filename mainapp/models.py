from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.abstract_models import AbstractItemModel, AbstrcatGroupModel


class StampGroup(AbstrcatGroupModel):
    """Группы печатей."""

    pic_upload_place = "group_pics/"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Группа печатей"
        verbose_name_plural = "Группы печатей"

    def __str__(self):
        return self.title

    def get_admin_url(self):
        # TODO: это можно перенести в файл админки?
        """Получение ссылки на модель. Для админки."""
        url = reverse(
            "admin:%s_%s_change"
            % (self._meta.app_label, self._meta.model_name),
            args=[self.pk],
        )
        return mark_safe('<a href="{}">{}</a>'.format(url, self.title))


class Stamp(AbstractItemModel):
    """Печать."""

    pic_upload_place = "stamps/"

    group = models.ForeignKey(
        to=StampGroup,
        on_delete=models.RESTRICT,
        related_name="stamps",
        verbose_name="Группа",
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
