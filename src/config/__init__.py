from pathlib import Path
from .celery import app as celery_app

#  Чтобы  Celery загружается при запуске Django.
__all__ = ("celery_app",)

#  Used in splitted_settings files, for avoiding circular imports
BASE_DIR = Path(__file__).resolve().parent.parent
