from django.db import models


class AbstrcatGroupModel(models.Model):
    """Абстрактная модель группы."""

    pic_upload_place = ""

    title = models.CharField(
        verbose_name="Заголовок",
        unique=True,
        max_length=200,
        help_text="Название группы",
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        help_text="Уникальный текстовый идентификатор группы",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to=pic_upload_place,
        help_text="Загрузить картинку",
    )
    published = models.BooleanField(
        verbose_name="Опубликованно",
        help_text="Включение и выключение отображения на сайте",
    )
    created = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    min_group_price = models.PositiveIntegerField(
        default=0, verbose_name="Минимальная цена"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class AbstractItemModel(models.Model):
    """Абстрактная модель предмета."""

    pic_upload_place = ""

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=200,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        help_text="Уникальный текстовый идентификатор группы",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    price = models.PositiveIntegerField(verbose_name="Цена")
    created = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    published = models.BooleanField(
        verbose_name="Опубликованно",
        help_text="Включение и выключение отображение на сайте",
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to=pic_upload_place,
    )

    class Meta:
        abstract = True
