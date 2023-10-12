from django.contrib import admin
from django.utils.safestring import mark_safe

from mainapp.models import Stamp, StampGroup


@admin.register(StampGroup)
class StampGroupAdmin(admin.ModelAdmin):
    exclude = ("slug", "min_group_price")
    list_display = (
        "title",
        "published",
        "created",
        "min_group_price",
        "image_tumbnail",
    )
    search_fields = ("title",)
    empty_value_display = "-пусто-"
    ordering = ("-created",)
    list_filter = ("published",)
    readonly_fields = ("image_preview",)

    @admin.display(description="Загруженная картинка")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" />'.format(obj.image.url))
        return "Картинка еще не загружена."

    @admin.display(description="Картинка")
    def image_tumbnail(self, obj):
        """Поле с иконкой картинки."""
        return mark_safe(f'<img src={obj.image.url} width="80" height="80">')


@admin.register(Stamp)
class StampAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "group",
        "description",
        "price",
        "published",
        "image",
        "image_preview",
    )
    exclude = ("slug",)
    autocomplete_fields = ("group",)
    list_display = (
        "title",
        "group_link",
        "description",
        "price",
        "published",
        "created",
        "image_tumbnail",
    )
    list_filter = (
        "group",
        "published",
    )
    readonly_fields = ("image_preview",)
    search_fields = ("title",)

    @admin.display(description="Загруженная картинка")
    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" />'.format(obj.image.url))
        return "Картинка еще не загружена."

    @admin.display(description="Картинка")
    def image_tumbnail(self, obj):
        """Поле с иконкой картинки."""
        return mark_safe(f'<img src={obj.image.url} width="80" height="80">')

    @admin.display(description="Группа")
    def group_link(self, obj):
        """Поле группы - ссылка на редактированние группы."""
        return obj.group.get_admin_url()
