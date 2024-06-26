from django.db.models import Min
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from mainapp.models import Stamp


def update_min_price(instance):
    """Обновление минимальной цены.

    Как работает функция:
    - Ищем печать с минимальной ценой по группе.
    - Если нашли обновляем значение минимальной цены группы.
    - Если нет, то устанавливаем минимальную цену в 0.
    """
    new_group_price = (
        Stamp.objects.filter(group=instance.group, published=True)
        .aggregate(Min("price"))
        .get("price__min")
    )
    if new_group_price:
        instance.group.min_group_price = new_group_price
    else:
        instance.group.min_group_price = 0
    instance.group.save()


@receiver(post_save, sender=Stamp)
def stamp_post_save(sender, instance, created, *args, **kwargs):
    """Обновление минимальной цены при создание новой печати."""
    update_min_price(instance)


@receiver(post_delete, sender=Stamp)
def stamp_pre_delete(sender, instance, *args, **kwargs):
    """Обновление минимальной цены при удаление печати."""
    update_min_price(instance)
