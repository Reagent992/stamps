from django.contrib import admin

from stamp_fields.models import FieldsTypes, GroupOfFieldsTypes


@admin.register(FieldsTypes)
class FieldsTypesAdmin(admin.ModelAdmin):
    """Настройка админки для Типов полей формы."""

    list_display = ("name", "re", "help_text", "created")
    ordering = ("-created",)


@admin.register(GroupOfFieldsTypes)
class GroupOfFieldsTypesAdmin(admin.ModelAdmin):
    """Настройка админки для Групп типов полей."""

    list_display = ("name", "created")
    filter_horizontal = ("fields",)
    ordering = ("-created",)
