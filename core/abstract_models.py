from django.db import models


class PublishedManager(models.Manager):
    """Расширение стандартного модельного менеджера."""

    def published(self):
        """Queryset только из опубликованных объектов."""
        return super().get_queryset().filter(published=True)


class AbstractTimeModel(models.Model):
    """Абстрактная модель времени."""

    created = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True


class AbstractGroupModel(AbstractTimeModel):
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
        verbose_name="Опубликовано",
        help_text="Включение и выключение отображения на сайте",
    )
    min_group_price = models.PositiveIntegerField(
        default=0, verbose_name="Минимальная цена"
    )
    objects = PublishedManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class AbstractItemModel(AbstractTimeModel):
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
    published = models.BooleanField(
        verbose_name="Опубликовано",
        help_text="Включение и выключение отображение на сайте",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to=pic_upload_place,
    )
    objects = PublishedManager()

    class Meta:
        abstract = True
