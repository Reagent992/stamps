from django.contrib import admin

from mainapp.admin import StampAdmin, StampGroupAdmin
from printy.models import Printy, PrintyGroup


@admin.register(PrintyGroup)
class PrintyGroupAdmin(StampGroupAdmin):
    """Настройка админки для Групп Оснасток."""

    pass


@admin.register(Printy)
class PrintyAdmin(StampAdmin):
    """Настройка админки для Оснасток."""

    fields = (
        "title",
        "group",
        "description",
        "price",
        "published",
        "image",
        "image_preview",
        # "printy",  Исключение лишнего поля.
    )
    filter_horizontal = ()
