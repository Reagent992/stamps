from .celery import app as celery_app

#  Чтобы  Celery загружается при запуске Django.
__all__ = ("celery_app",)
