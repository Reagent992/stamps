import logging

from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from slugify import slugify

from core.tasks import paste_watermark_and_resize_image

logger = logging.getLogger("__name__")


class PublishedManager(models.Manager):
    """Расширение стандартного модельного менеджера."""

    def get_queryset(self) -> models.QuerySet:
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


class AbstractGroupModel(DirtyFieldsMixin, AbstractTimeModel):
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
    objects = models.Manager()
    filter_published = PublishedManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)


class AbstractItemModel(DirtyFieldsMixin, AbstractTimeModel):
    """Абстрактная модель предмета."""

    pic_upload_place = ""  # FIXME: не переопределяется в моделях-наследниках.
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
    objects = models.Manager()
    filter_published = PublishedManager()
    _skip_celery_task = False

    class Meta:
        abstract = True

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        self.slug = slugify(self.title)
        created = self.pk is None
        logger.debug(
            (
                f"Saving new {self.__class__.__name__} object, "
                f"created: {created}, "
                f"self:{self}, "
                f"force_insert:{force_insert}, "
                f"force_update:{force_update}, "
                f"fields:{update_fields}"
                f"celery task flag: {self._skip_celery_task}"
            )
        )
        is_dirty = self.is_dirty()
        self.image_changed = self.get_dirty_fields().get("image")
        self.temp_image_name = None
        super().save(force_insert, force_update, using, update_fields)
        if not self._skip_celery_task:
            if created and self.image:
                self.send_celery_task()
            elif (
                not created
                and is_dirty
                and self.image_changed
                and update_fields is None
            ):
                self.send_celery_task()

    def send_celery_task(self) -> None:
        logger.info("Sending new image to edit")
        paste_watermark_and_resize_image.apply_async(
            (
                self.__class__.__name__,
                self.id,
                self._meta.app_label,
                self.image_changed,
                self.image.name,
            ),
            countdown=settings.TASK_BEGIN_DELAY,
        )
