from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка админки для Заказов."""

    list_display = (
        "id",
        "email",
        # "stamp",
        # "printy",
        "comment",
        # "stamp_text",
        "name",
        # "address",
        # "city",
        # "postal_code",
        "phone",
        "created",
        # "updated",
    )
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }
    ordering = ("-updated",)
    list_filter = ("stamp", "printy", "city")
    search_fields = (
        "email",
        "phone",
        "name",
        "address",
        "city",
        "postal_code",
        "comment",
        "stamp__title",
        "printy__title",
    )
