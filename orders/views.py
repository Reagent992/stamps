from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.forms import StampTextForm
from mainapp.models import Stamp
from mainapp.tasks import send_order_email
from orders.forms import OrderForm
from orders.models import Order
from printy.models import Printy


class CreateStampOrderView(TitleBreadcrumbsMixin, TemplateView):
    """Создание заказа на печать."""

    template_name = settings.ORDER_FORM_TEMPLATE
    title = settings.ORDER_TITLE

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        selected_stamp = get_object_or_404(
            Stamp.objects.published(),
            id=self.request.session.get("selected_stamp_id"),
        )
        return [
            (
                selected_stamp.group.title,
                reverse_lazy(
                    "mainapp:stamps",
                    kwargs={"group": selected_stamp.group.slug},
                ),
            ),
            (
                selected_stamp.title,
                reverse_lazy(
                    "mainapp:item_details",
                    kwargs={
                        "group": selected_stamp.group.slug,
                        "slug_item": selected_stamp.slug,
                    },
                ),
            ),
            (
                "Заказ",
                reverse_lazy(
                    "orders:create_order",
                    kwargs={
                        "group": selected_stamp.group.slug,
                        "slug_item": selected_stamp.slug,
                    },
                ),
            ),
        ]

    def get_context_data(self, **kwargs):
        """Передача формы и остального в шаблон."""
        context = super().get_context_data(**kwargs)
        selected_stamp = get_object_or_404(
            Stamp.objects.published(), slug=self.kwargs["slug_item"]
        )
        selected_printy = get_object_or_404(
            Printy.objects.published(),
            id=self.request.session.get("selected_printy_id"),
        )
        stamp_fields = selected_stamp.form_fields.fields.all()
        stamp_text_form = StampTextForm(stamp_fields)
        order_form = OrderForm()
        context["form"] = stamp_text_form
        context["order_form"] = order_form
        context["item"] = selected_stamp
        context["selected_printy"] = selected_printy
        context["price_sum"] = selected_printy.price + selected_stamp.price
        return context

    def post(self, request, *args, **kwargs):
        """Заполненная форма для заказа."""
        selected_stamp = get_object_or_404(
            Stamp.objects.published(), slug=self.kwargs["slug_item"]
        )
        selected_printy = get_object_or_404(
            Printy.objects.published(),
            id=request.session.get("selected_printy_id"),
        )
        stamp_fields = selected_stamp.form_fields.fields.all()
        stamp_text_form = StampTextForm(stamp_fields, request.POST or None)
        order_form = OrderForm(request.POST or None)

        if stamp_text_form.is_valid() and order_form.is_valid():
            order = Order.objects.create(
                **order_form.cleaned_data,
                stamp_text=stamp_text_form.cleaned_data,
                printy=selected_printy,
                stamp=selected_stamp,
            )
            send_order_email.delay(order_id=order.id)
            return redirect("orders:order_success")

        return render(
            request,
            self.template_name,
            {
                "context": self.get_context_data(),
                "form": stamp_text_form,
                "order_form": order_form,
                "item": selected_stamp,
                "selected_printy": selected_printy,
                "price_sum": selected_printy.price + selected_stamp.price,
                "title": self.title,
            },
        )


class SuccessFormView(TitleBreadcrumbsMixin, TemplateView):
    """Страница успешно созданного заказа."""

    template_name = settings.ORDER_SUCCESS_TEMPLATE
    title = settings.ORDER_CREATED
    crumbs = []
