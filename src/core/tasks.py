from io import BytesIO
from typing import NamedTuple
from uuid import uuid4

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType

from core.utils import get_object_by_model_id_app

logger = get_task_logger(__name__)


class Position(NamedTuple):
    x: int
    y: int


class RGBA_Color(NamedTuple):
    red: int
    green: int
    blue: int
    alpha: int


IMAGE_SIZE_IN_PIXELS = settings.IMAGE_SIZE_IN_PIXELS
TEXT_COLOR = RGBA_Color(*settings.TEXT_COLOR)
TEXT_POSITION = Position(*settings.TEXT_POSITION)
FONT_SIZE = settings.FONT_SIZE
WATERMARK_TEXT = settings.WATERMARK_TEXT
USE_WATERMARK_FILE = settings.USE_WATERMARK_FILE
WATERMARK_PATH = settings.WATERMARK_PATH
IMAGE_FORMAT = settings.IMAGE_FORMAT
FONT = settings.FONT


def open_image(path_to_image: str) -> ImageType:
    try:
        image = Image.open(path_to_image)
    except FileNotFoundError as e:
        msg = f"FileNotFoundError occurred while opening file: {e}"
        logger.error(msg, exc_info=e)
        raise FileNotFoundError(msg)
    image = image.convert("RGBA")
    return image


def paste_watermark_file(
    image: ImageType, path_to_watermark: str
) -> ImageType:
    watermark = open_image(path_to_watermark)
    watermark = watermark.resize(IMAGE_SIZE_IN_PIXELS)
    image.paste(watermark, None, watermark)
    return image


def paste_text_watermark(
    image: ImageType,
    text: str = WATERMARK_TEXT,
    font: str = FONT,
    color: RGBA_Color = TEXT_COLOR,
    position: Position = TEXT_POSITION,
    font_size: int = FONT_SIZE,
) -> ImageType:
    """
    :param image: Image class obj.
    :param text: text to be placed on image.
    :param font: path to font.
    :param color: RGBA color as tuple like (255, 255, 255, 0).
    :param position: relative position from RIGHT BOTTOM corner.
    :param size: font size as int.
    """
    blank_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(blank_image, "RGBA")
    relative_position: tuple[int, int] = (
        image.height - position.x,
        image.width - position.y,
    )
    draw.text(relative_position, text, color, font, "rb")
    return Image.alpha_composite(image, blank_image)


@shared_task
def paste_watermark_and_resize_image(
    model_name: str,
    object_id: str | int,
    app_label: str,
    old_image_name: str = None,
    temp_image_name: str = None,
) -> None:
    """Celery task that places a watermark on image
    and resizes it to the default size"""
    instance = get_object_by_model_id_app(model_name, object_id, app_label)
    logger.info(f"Start of celery task for {instance}")
    absolute_path_to_image = instance.image.path
    image = open_image(absolute_path_to_image)
    image = image.resize(IMAGE_SIZE_IN_PIXELS, Image.Resampling.LANCZOS)
    if USE_WATERMARK_FILE:
        image = paste_watermark_file(image, WATERMARK_PATH)
    else:
        image = paste_text_watermark(image)
    # prepare new image to save
    new_file_name = uuid4().hex
    buffer = BytesIO()
    image.save(fp=buffer, format=IMAGE_FORMAT)
    image_file = ContentFile(buffer.getvalue())
    instance._skip_celery_task = True
    # save new image file
    instance.image.save(new_file_name + "." + IMAGE_FORMAT, image_file)
    # save new image name
    instance.save(update_fields=["image"])
    instance._skip_celery_task = False

    if old_image_name and old_image_name != instance.image.name:
        logger.info(f"Deleting old image file: {old_image_name}")
        default_storage.delete(old_image_name)
    if temp_image_name and temp_image_name != instance.image.name:
        logger.info(f"Deleting temp image file: {temp_image_name}")
        default_storage.delete(temp_image_name)
