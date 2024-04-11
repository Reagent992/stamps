from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

from core.abstract_models import AbstractTimeModel
from mainapp.models import Stamp
from printy.models import Printy


class Order(AbstractTimeModel):
    """Заказ."""

    email = models.EmailField("email", max_length=254)
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[MinLengthValidator(6)],
    )
    name = models.CharField("Имя", max_length=100)
    address = models.CharField("Адрес", max_length=200)
    city = models.CharField("Город", max_length=100)
    postal_code = models.CharField(
        "Почтовый индекс", max_length=20, blank=True, default=""
    )
    stamp = models.ForeignKey(
        to=Stamp,
        on_delete=models.RESTRICT,
        verbose_name="Печать",
    )
    printy = models.ForeignKey(
        to=Printy,
        on_delete=models.RESTRICT,
        verbose_name="Оснастка",
    )
    stamp_text = models.JSONField("Содержание печати", blank=True)
    comment = models.TextField("Комментарий", blank=True, default="")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"Заказ №{self.pk}"
