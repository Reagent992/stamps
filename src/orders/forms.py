from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    """Форма заказа."""

    class Meta:
        model = Order
        fields = (
            "email",
            "phone",
            "name",
            "address",
            "city",
            "postal_code",
            "comment",
        )
