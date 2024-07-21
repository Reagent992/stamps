import logging
from pathlib import Path
from uuid import uuid4

from django.apps import apps
from django.db.models import Model

logger = logging.getLogger("logger")


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
