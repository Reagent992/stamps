from typing import Optional

from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.safestring import mark_safe

from mainapp.models import Stamp, StampGroup
from printy.models import PrintyGroup

admin.site.unregister(Group)


@admin.register(StampGroup)
class StampGroupAdmin(admin.ModelAdmin):
    """Настройка админки для Групп Печатей."""

    exclude = ("slug", "min_group_price")
    list_display = (
        "title",
        "published",
        "created",
        "updated",
        "min_group_price",
        "get_obj_count",
        "image_thumbnail",
    )
    search_fields = ("title",)
    empty_value_display = "-пусто-"
    ordering = ("-created",)
    list_filter = ("published",)
    readonly_fields = ("image_preview",)

    @admin.display(description="Текущая картинка")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" />'.format(obj.image.url))
        return "Картинка еще не загружена."

    @admin.display(description="Картинка")
    def image_thumbnail(self, obj):
        """Поле с иконкой картинки."""
        return mark_safe(f'<img src={obj.image.url} width="80" height="80">')

    @admin.display(description="Количество")
    def get_obj_count(self, obj: StampGroup | PrintyGroup) -> Optional[int]:
        if hasattr(obj, "stamps"):
            return obj.stamps.count()
        if hasattr(obj, "printy"):
            return obj.printy.count()
        return None


@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    """Настройка админки для Печатей."""

    fields = (
        "title",
        "group",
        "description",
        "price",
        "published",
        "image",
        "image_preview",
        "printy",
        "form_fields",
    )
    filter_horizontal = ("printy",)
    exclude = ("slug",)
    autocomplete_fields = ("group",)
    list_display = (
        "title",
        "group_link",
        "description",
        "price",
        "published",
        "created",
        "updated",
        "image_thumbnail",
    )
    list_filter = (
        "group",
        "published",
    )
    readonly_fields = ("image_preview",)
    search_fields = ("title",)

    @admin.display(description="Текущая картинка")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="300" height="300">'
            )
        return "Картинка еще не загружена."

    @admin.display(description="Иконка")
    def image_thumbnail(self, obj):
        """Поле с иконкой картинки."""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="80">'
            )
        return "Нет иконки"

    @admin.display(description="Группа")
    def group_link(self, obj):
        """Поле группы - ссылка на редактирование группы."""
        url = reverse(
            "admin:%s_%s_change"
            % (obj.group._meta.app_label, obj.group._meta.model_name),
            args=[obj.group.pk],
        )
        return mark_safe('<a href="{}">{}</a>'.format(url, obj.group.title))
