from django.db import models

from core.abstract_models import AbstractItemModel, AbstrcatGroupModel


class Group(AbstrcatGroupModel):
    """Группы печатей."""
    pic_upload_place = 'group_pics/'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title

    def min_price(self):
        """
        Самый дешевый товар в группе.
        # FIXME: Переделать.
        """
        min_price = None
        for stamp in self.stamps.all():
            if min_price is None or stamp.price < min_price:
                min_price = stamp.price
        return min_price


class Stamp(AbstractItemModel):
    """Печать."""
    pic_upload_place = 'stamps/'

    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        related_name='stamps',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться штамп',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Печать'
        verbose_name_plural = 'Печати'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'group'],
                name='unique_title_group')
        ]

    def __str__(self):
        return self.title
