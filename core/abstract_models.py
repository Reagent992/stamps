from django.db import models


class AbstrcatGroupModel(models.Model):
    """Абстрактная модель группы."""
    pic_upload_place = ''

    title = models.CharField(
        unique=True,
        max_length=200,
        help_text='Название группы'
    )
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный текстовый идентификатор группы'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=pic_upload_place,
        help_text='Загрузить картинку',
    )
    published = models.BooleanField(
        help_text='Включение и выключение отображение на сайте'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class AbstractItemModel(models.Model):
    """Абстрактная модель предмета."""
    pic_upload_place = ''

    title = models.CharField(
        max_length=200,
        help_text='Название'
    )
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный текстовый идентификатор предмета'
    )
    description = models.TextField(
        help_text='Описание'
    )
    price = models.PositiveIntegerField(
        help_text='Цена'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    published = models.BooleanField(
        help_text='Включение и выключение отображение на сайте'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=pic_upload_place,
        help_text='Загрузить картинку',
    )

    class Meta:
        abstract = True
