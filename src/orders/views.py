import logging

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView

from core.mixins import ItemsFromSessionMixin, TitleBreadcrumbsMixin
from mainapp.forms import StampTextForm
from orders.forms import OrderForm
from orders.models import Order
from orders.tasks import send_order_email

logger = logging.getLogger(__name__)


class CreateStampOrderView(
    TitleBreadcrumbsMixin, TemplateView, ItemsFromSessionMixin
):
    """Create new order."""

    template_name = settings.ORDER_FORM_TEMPLATE
    title = settings.ORDER_TITLE

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        return [
            (
                f"Печать: {self.selected_stamp.title}",
                reverse_lazy(
                    "mainapp:item_details",
                    kwargs={
                        "group": self.selected_stamp.group.slug,
                        "slug_item": self.selected_stamp.slug,
                    },
                ),
            ),
            (
                f"Оснастка: {self.selected_printy.title}",
                reverse_lazy(
                    "printy:printy_details",
                    kwargs={
                        "printy_group": self.selected_printy.group.slug,
                        "printy_item": self.selected_printy.slug,
                    },
                ),
            ),
            (
                "Заказ",
                reverse_lazy(
                    "orders:create_order",
                ),
            ),
        ]

    def get_context_data(self, **kwargs):
        """Fill context."""
        context = super().get_context_data(**kwargs)
        stamp_fields = self.selected_stamp.form_fields.fields.all()
        stamp_text_form = StampTextForm(stamp_fields)
        order_form = OrderForm()
        context["form"] = stamp_text_form
        context["order_form"] = order_form
        context["item"] = self.selected_stamp
        context["selected_printy"] = self.selected_printy
        context["price_sum"] = (
            self.selected_printy.price + self.selected_stamp.price
        )
        return context

    def post(self, request, *args, **kwargs):
        """Submitted order form."""
        stamp_fields = self.selected_stamp.form_fields.fields.all()
        stamp_text_form = StampTextForm(stamp_fields, request.POST or None)
        order_form = OrderForm(request.POST or None)

        if stamp_text_form.is_valid() and order_form.is_valid():
            order = Order.objects.create(
                **order_form.cleaned_data,
                stamp_text=stamp_text_form.cleaned_data,
                printy=self.selected_printy,
                stamp=self.selected_stamp,
            )
            if settings.DEBUG:
                logger.info(
                    (
                        "New Order was created. id=%d, stamp=%s, printy=%s, "
                        "order_info=%s, stamp_text=%s"
                    ),
                    order.id,
                    self.selected_stamp,
                    self.selected_printy,
                    order_form.cleaned_data,
                    stamp_text_form.cleaned_data,
                )
            send_order_email.delay(
                (order.id, order.email),
                countdown=settings.TASK_BEGIN_DELAY,
            )
            return redirect("orders:order_success")

        return render(
            request,
            self.template_name,
            {
                "context": self.get_context_data(),
                "form": stamp_text_form,
                "order_form": order_form,
                "item": self.selected_stamp,
                "selected_printy": self.selected_printy,
                "price_sum": self.selected_printy.price
                + self.selected_stamp.price,
                "title": self.title,
            },
        )


class SuccessFormView(TitleBreadcrumbsMixin, TemplateView):
    """Successfully created order."""

    template_name = settings.ORDER_SUCCESS_TEMPLATE
    title = settings.ORDER_CREATED
    crumbs = []
