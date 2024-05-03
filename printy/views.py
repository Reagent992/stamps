from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.models import Stamp
from printy.models import Printy, PrintyGroup


class PrintyGroupsView(TitleBreadcrumbsMixin, ListView):
    """Группы оснасток."""

    model = PrintyGroup
    queryset = PrintyGroup.objects.published()
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.PRINTY_TITLE
    home_label = settings.PRINTY_LABEL
    crumbs = []

    def get_queryset(self):
        """Опциональная фильтрация групп оснасток по выбранной печати,
        через параметры запроса."""
        self.stamp_id = self.request.GET.get("stamp_id")
        if not self.stamp_id:
            return super().get_queryset()
        stamp_obj = get_object_or_404(
            Stamp.objects.published(), id=self.stamp_id
        )
        list_of_group_ids = stamp_obj.printy.values_list(
            "group", flat=True
        ).distinct()
        return PrintyGroup.objects.published(id__in=list_of_group_ids)

    def get_context_data(self, **kwargs):
        """Передаем название View в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "button_text": settings.ABOUT_GROUP,
            "param": self.stamp_id,
            "PrintyGroupsView": True,
        }


class PrintyGroupContentView(TitleBreadcrumbsMixin, ListView):
    """Оснастки отфильтрованные по группе."""

    model = PrintyGroup
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABEL

    def get_queryset(self):
        """Выводим только подходящие для выбранной(через params)
        печати оснастки или все."""
        self.printy_group = get_object_or_404(
            PrintyGroup.objects.published(), slug=self.kwargs["printy_group"]
        )
        self.stamp_id = self.request.GET.get("stamp_id")
        if self.stamp_id:
            stamp_obj = get_object_or_404(
                Stamp.objects.published(), id=self.stamp_id
            )
            return stamp_obj.printy.published(group=self.printy_group)
        return Printy.objects.published(group=self.printy_group)

    def get_title(self):
        """Заголовок вкладки."""
        return self.printy_group.title

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаем название View в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "button_text": settings.ABOUT_PRINTY,
        }

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        return [(self.printy_group.title, reverse_lazy("printy:printys"))]


class PrintyView(TitleBreadcrumbsMixin, DetailView):
    """Подробности об оснастке."""

    model = Printy
    template_name = settings.ITEM_DETAIL_TEMPLATE
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABEL

    def get_object(self, queryset=None):
        return get_object_or_404(
            Printy.objects.published(),
            slug=self.kwargs["printy_item"],
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Если печать уже выбрана, показываем кнопку сделать заказ."""
        selected_stamp_id = self.request.session.get("selected_stamp_id")
        context = super().get_context_data(**kwargs)
        context["turn_off_button"] = not bool(selected_stamp_id)
        context["button_text"] = settings.BUTTON_MAKE_ORDER
        self.selected_stamp_obj: Stamp = get_object_or_404(
            Stamp.objects.published(), id=selected_stamp_id
        )
        if self.get_object() not in self.selected_stamp_obj.printy.all():
            context["disable_button"] = True
            context["button_text"] = settings.BUTTON_WRONG_PRINTY
        return context

    def post(self, request, *args, **kwargs):
        """Запись выбранной оснастки в сессию."""
        if "chosen_item_id" in request.POST:
            selected_stamp_id = self.request.session.get("selected_stamp_id")
            chosen_item_id = request.POST["chosen_item_id"]
            self.request.session["selected_printy_id"] = chosen_item_id
            selected_stamp_obj = get_object_or_404(
                Stamp.objects.published(), id=selected_stamp_id
            )
            selected_stamp_obj.slug
            selected_stamp_obj.group.slug
            return redirect(
                "orders:create_order",
                selected_stamp_obj.group.slug,
                selected_stamp_obj.slug,
            )
        return super().get(request, *args, **kwargs)

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        printy_group = get_object_or_404(
            PrintyGroup.objects.published(), slug=self.kwargs["printy_group"]
        )
        return [
            (
                printy_group.title,
                reverse_lazy(
                    "printy:printys",
                    kwargs={"printy_group": printy_group.slug},
                ),
            ),
            (self.object.title, reverse_lazy("printy:printy_details")),
        ]
