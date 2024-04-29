from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView, TemplateView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.forms import StampTextForm
from mainapp.models import Stamp, StampGroup
from mainapp.tasks import send_order_email
from orders.forms import OrderForm
from orders.models import Order
from printy.models import Printy


class StampGroupView(TitleBreadcrumbsMixin, ListView):
    """Главная страница, группы печатей."""

    model = StampGroup
    queryset = StampGroup.objects.published()
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.INDEX_TITLE
    crumbs = []

    def get_context_data(self, **kwargs):
        """Передаем данные в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "button_text": settings.ABOUT_GROUP,
            "IndexView": True,
        }


class GroupedStampsView(TitleBreadcrumbsMixin, ListView):
    """Печати отфильтрованные оп группе."""

    model = StampGroup
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT

    def get_queryset(self):
        self.stamp_group = get_object_or_404(
            StampGroup.objects.published(), slug=self.kwargs["group"]
        )
        return Stamp.objects.published(group=self.stamp_group)

    def get_title(self):
        """Заголовок вкладки."""
        return self.stamp_group.title

    def get_context_data(self, *args, object_list=None, **kwargs):
        """Передаем название View в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "button_text": settings.ABOUT_STAMP,
        }

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        return [(self.stamp_group.title, reverse_lazy("mainapp:stamps"))]


class StampDetailView(TitleBreadcrumbsMixin, DetailView):
    """Подробности о печати."""

    model = Stamp
    template_name = settings.ITEM_DETAIL_TEMPLATE

    def get_object(self, queryset=None):
        return get_object_or_404(
            Stamp.objects.published(), slug=self.kwargs["slug_item"]
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Передача данных в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "printy_selected": bool(
                self.request.session.get("selected_printy_id")
            ),
            "button_text": settings.BUTTON_CHOICE_PRINTY,
        }

    def post(self, request, *args, **kwargs):
        """Запись выбранной печати в сессию и редирект на выбор оснастки."""
        if "chosen_item_id" in request.POST:
            chosen_item_id = request.POST["chosen_item_id"]
            self.request.session["selected_stamp_id"] = chosen_item_id
            return redirect(
                reverse("printy:printy_index") + f"?stamp_id={chosen_item_id}"
            )
        return super().post(request, *args, **kwargs)

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        current_stamp_group = get_object_or_404(
            StampGroup.objects.published(), slug=self.kwargs["group"]
        )
        return [
            (
                current_stamp_group.title,
                reverse_lazy(
                    "mainapp:stamps",
                    kwargs={"group": current_stamp_group.slug},
                ),
            ),
            (self.object.title, reverse_lazy("mainapp:item_details")),
        ]


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
                    "mainapp:stamp_form",
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
            return redirect("mainapp:order_success")

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
