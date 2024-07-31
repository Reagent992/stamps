import logging
from pathlib import Path
from uuid import uuid4

from django.apps import apps
from django.conf import settings
from django.db.models import Model

logger = logging.getLogger(__name__)


def get_object_by_model_id_app(
    model_name: str, object_id: str | int, app_label: str
) -> Model:
    try:
        model_class = apps.get_model(
            app_label=app_label, model_name=model_name
        )
        obj = model_class.objects.get(id=int(object_id))
        return obj
    except model_class.DoesNotExist as error:
        logger.error(f"Error occur wile trying to get object: {error}")
        raise model_class.DoesNotExist


def get_renamed_image_path(instance: Model, filename: str) -> str:
    new_file_name = uuid4().hex
    file_extension = Path(filename).suffix
    logger.info(
        (
            f"File: {filename}, "
            f"Instance: {instance}, "
            f"Old file name: {filename}, "
            f"New file name: {new_file_name}{file_extension},"
        )
    )
    return (
        f"{instance.__class__.__name__.lower()}"
        "/"
        f"{new_file_name}"
        f"{file_extension}"
    )


def get_tg_msg(order) -> str:
    fields = "\n".join([f"➖ {x}: {y}" for x, y in order.stamp_text.items()])
    stamp_url = settings.HOST + order.printy.get_absolute_url()
    printy_url = settings.HOST + order.stamp.get_absolute_url()
    return f"""
📦 *Новый заказ №{order.id}*

➖ Печать: [{order.stamp.title}]({stamp_url})
➖ Штамп: [{order.printy.title}]({printy_url})

✏️ *Надпись на печати*
{fields}

🧑‍🔧 *Заказчик*
➖ Email: {order.email}
➖ Телефон: {order.phone}
➖ Имя: {order.name}
➖ Адрес: {order.address}
➖ Город: {order.city}
➖ Почтовый индекс: {order.postal_code}
➖ Комментарий: {order.comment}
"""
