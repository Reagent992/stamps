from django.db.models import Min
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from slugify import slugify

from printy.models import Printy, PrintyGroup


@receiver(pre_save, sender=PrintyGroup)
def stamp_group_create_pre_save(sender, instance, *args, **kwargs):
    """Заполнение поля slug при создании новой группы оснасток."""
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(pre_save, sender=Printy)
def stamp_create_pre_save(sender, instance, *args, **kwargs):
    """Заполнение поля slug при создании новой оснастки."""
    if not instance.slug:
        instance.slug = slugify(instance.title)


def update_min_price(instance):
    """Обновление минимальной цены.

    Как работает функция:
    - Ищем оснастку с минимальной ценой по группе.
    - Если нашли обновляем значение минимальной цены группы.
    - Если нет, то устанавливаем минимальную цену в 0.
    """
    new_group_price = (
        Printy.objects.filter(group=instance.group, published=True)
        .aggregate(Min("price"))
        .get("price__min")
    )
    if new_group_price:
        instance.group.min_group_price = new_group_price
    else:
        instance.group.min_group_price = 0
    instance.group.save()


@receiver(post_save, sender=Printy)
def stamp_post_save(sender, instance, created, *args, **kwargs):
    """Обновление минимальной цены при создание новой оснастки."""
    update_min_price(instance)


@receiver(post_delete, sender=Printy)
def stamp_pre_delete(sender, instance, *args, **kwargs):
    """Обновление минимальной цены при удаление оснастки."""
    update_min_price(instance)
