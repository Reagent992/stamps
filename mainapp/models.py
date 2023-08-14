from django.db import models


class Group(models.Model):
    """Группы печатей."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='group_pics/',
        blank=False,
        help_text='Загрузить картинку',
        # TODO: default=''  Добавить заглушку
    )
    published = models.BooleanField()

    def min_price(self):
        """
        Самый дешевый товар в группе.
        # TODO: Ужасный способ.
        """
        min_price = None
        for stamp in self.stamps.all():
            if min_price is None or stamp.price < min_price:
                min_price = stamp.price
        return min_price

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Stamp(models.Model):
    """Печать."""
    group = models.ForeignKey(
        to=Group,
        on_delete=models.RESTRICT,
        related_name='stamps',
        blank=False,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться штамп',
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='stamps/',
        blank=False,
        help_text='Загрузить картинку',
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        db_index=True,
    )
    published = models.BooleanField()

    class Meta:
        ordering = ['-created']
        verbose_name = 'Печать'
        verbose_name_plural = 'Печати'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'group'],
                name='unique_title_group')
        ]

    def __str__(self):
        return self.title
