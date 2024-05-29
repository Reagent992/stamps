from django.db.models import Min
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from printy.models import Printy


def update_min_price(instance) -> None:
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
def stamp_post_save(sender, instance, created, *args, **kwargs) -> None:
    """Обновление минимальной цены при создание новой оснастки."""
    update_min_price(instance)


@receiver(post_delete, sender=Printy)
def stamp_pre_delete(sender, instance, *args, **kwargs) -> None:
    """Обновление минимальной цены при удаление оснастки."""
    update_min_price(instance)
