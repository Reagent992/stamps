import os

from celery import Celery

#  Установка значения для константы, если она отсутствует,
#  через стандартный метод словаря.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
#  Создание экземпляра Celery, в качестве аргумента имя главного модуля.
app = Celery("config")
#  Определение файла настроек Django как конфигурационный файл для Celery.
#  namespace влияет на написание констант для Celery
app.config_from_object("django.conf:settings", namespace="CELERY")
#  Указание экземпляру приложения Celery автоматически находить
#  все задачи в каждом приложении вашего проекта Django.
#  Задачи создаются в ./<app_name>/tasks.py
app.autodiscover_tasks()
