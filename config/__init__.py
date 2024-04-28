from .celery import app as celery_app

#  Чтобы  Celery загружается при запуске Django.
__all__ = ("celery_app",)
#  Гарантирует, что декоратор @shared_task будет работать корректно.
