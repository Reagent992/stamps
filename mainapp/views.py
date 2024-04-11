from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView, TemplateView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.forms import StampTextForm
from mainapp.models import Stamp, StampGroup
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
        """Передаем название View в шаблон."""
        return {**super().get_context_data(**kwargs), "IndexView": True}


class GroupedStampsView(TitleBreadcrumbsMixin, ListView):
    """Печати отфильтрованные оп группе."""

    model = StampGroup
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT

    def get_queryset(self):
        self.stamp_group = get_object_or_404(
            StampGroup, slug=self.kwargs["group"]
        )
        return Stamp.objects.filter(group=self.stamp_group, published=True)

    def get_title(self):
        """Заголовок вкладки."""
        return self.stamp_group.title

    def get_context_data(self, *args, object_list=None, **kwargs):
        """Передаем название View в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "GroupedStampsView": True,
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
            Stamp, slug=self.kwargs["slug_item"], published=True
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Запись выбранной печати в сессию."""
        # TODO: rename to selected_stamp_id
        self.request.session["stamp"] = self.object.id
        return super().get_context_data(**kwargs)

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        current_stamp_group = get_object_or_404(
            StampGroup, slug=self.kwargs["group"]
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
            Stamp, id=self.request.session.get("stamp")
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
            Stamp, slug=self.kwargs["slug_item"], published=True
        )
        selected_printy = get_object_or_404(
            Printy, id=self.request.session.get("printy"), published=True
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
            Stamp, slug=self.kwargs["slug_item"], published=True
        )
        selected_printy = get_object_or_404(
            Printy, id=request.session.get("printy"), published=True
        )
        stamp_fields = selected_stamp.form_fields.fields.all()
        stamp_text_form = StampTextForm(stamp_fields, request.POST or None)
        order_form = OrderForm(request.POST or None)

        if stamp_text_form.is_valid() and order_form.is_valid():
            Order.objects.create(
                **order_form.cleaned_data,
                stamp_text=stamp_text_form.cleaned_data,
                printy=selected_printy,
                stamp=selected_stamp,
            )
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
    """Страница успешного созданного заказа."""

    template_name = settings.ORDER_SUCCESS_TEMPLATE
    title = settings.ORDER_CREATED
    crumbs = []
