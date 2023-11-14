from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from core.views_helpers import get_stamp_obj
from mainapp.models import Stamp
from printy.models import Printy, PrintyGroup


class PrintyGroupsView(TitleBreadcrumbsMixin, ListView):
    """Группы оснасток."""

    model = PrintyGroup
    queryset = PrintyGroup.objects.filter(published=True)
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.PRINTY_TITLE
    home_label = settings.PRINTY_LABLE
    crumbs = []

    def get_queryset(self):
        """Выводим только подходящие для выбранной печати оснастки или все."""
        stamp_obj: Stamp = get_stamp_obj(self, Stamp)
        if stamp_obj:
            list_of_group_ids = stamp_obj.printy.values_list(
                "group", flat=True
            ).distinct()
            return PrintyGroup.objects.filter(
                id__in=list_of_group_ids, published=True
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Передаем название View в шаблон."""
        return {**super().get_context_data(**kwargs), "PrintyGroupsView": True}


class PrintyGroupContentView(TitleBreadcrumbsMixin, ListView):
    """Оснастки отфильтрованные по группе."""

    model = PrintyGroup
    template_name = settings.INDEX_TEMPLATE
    paginate_by = settings.PAGINATION_AMOUNT
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABLE

    def get_queryset(self):
        """Выводим только подходящие для выбранной печати оснастки или все."""
        self.printy_group = get_object_or_404(
            PrintyGroup, slug=self.kwargs["printy_group"]
        )
        stamp_obj: Stamp = get_stamp_obj(self, Stamp)
        if stamp_obj:
            return stamp_obj.printy.filter(
                group=self.printy_group, published=True
            )
        return Printy.objects.filter(group=self.printy_group, published=True)

    def get_title(self):
        """Заголовок вкладки."""
        return self.printy_group.title

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаем название View в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "PrintyGroupContentView": True,
        }

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        return [(self.printy_group.title, reverse_lazy("printy:printys"))]


class PrintyView(TitleBreadcrumbsMixin, DetailView):
    """Подробости об оснастке."""

    model = Printy
    template_name = settings.ITEM_DETAIL_TEMPLATE
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABLE

    def get_object(self, queryset=None):
        """Оснастка с проверкой на пригодность к выбранной печати."""
        stamp_obj: Stamp = get_stamp_obj(self, Stamp)
        if stamp_obj:
            # TODO: нужна кнопка
            # "выбранная оснастка не подходит для выбранной печати" вместо 404.
            return get_object_or_404(
                stamp_obj.printy,
                slug=self.kwargs["printy_item"],
                published=True,
            )
        return get_object_or_404(
            Printy, slug=self.kwargs["printy_item"], published=True
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Запись выбранной оснастки в сессию."""
        self.request.session["printy"] = self.object.id
        return super().get_context_data(**kwargs)

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        printy_group = get_object_or_404(
            PrintyGroup, slug=self.kwargs["printy_group"]
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
