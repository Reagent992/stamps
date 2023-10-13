from django.db import models

from core.abstract_models import AbstractItemModel, AbstrcatGroupModel


class PrintyGroup(AbstrcatGroupModel):
    """Группы оснасток для печатей."""

    pic_upload_place = "printy_group_pics/"

    class Meta:
        ordering = ("-created",)
        verbose_name = "Группа оснасток"
        verbose_name_plural = "Группы оснасток"

    def __str__(self):
        return self.title

    def min_price(self):
        """
        Самый дешевый товар в группе.
        # FIXME: Переделать.
        """
        min_price = None
        for printy in self.printy.all():
            if min_price is None or printy.price < min_price:
                min_price = printy.price
        return min_price


class Printy(AbstractItemModel):
    """Оснаска."""

    pic_upload_place = "printy_pics/"

    group = models.ForeignKey(
        to=PrintyGroup,
        on_delete=models.RESTRICT,
        related_name="printy",
        verbose_name="Группа оснасток",
        help_text="Группа, к которой будет относиться оснаска",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Оснастка"
        verbose_name_plural = "Оснастки"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "group"], name="unique_printy_title_group"
            )
        ]

    def __str__(self):
        return self.title