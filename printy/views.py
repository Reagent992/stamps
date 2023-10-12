from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from printy.models import Printy, PrintyGroup


class PrintyGroupsView(TitleBreadcrumbsMixin, ListView):
    """Группы оснасток."""

    model = PrintyGroup
    queryset = PrintyGroup.objects.filter(published=True)
    template_name = "mainapp/index.html"
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.PRINTY_TITLE
    home_label = settings.PRINTY_LABLE
    crumbs = []

    def get_context_data(self, **kwargs):
        """Передаем название View в шаблон."""
        return {**super().get_context_data(**kwargs), "PrintyGroupsView": True}


class PrintyGroupContentView(TitleBreadcrumbsMixin, ListView):
    """Оснастки отфильтрованные по группе."""

    model = PrintyGroup
    template_name = "mainapp/index.html"
    paginate_by = settings.PAGINATION_AMOUNT
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABLE

    def get_queryset(self):
        self.printy_group = get_object_or_404(
            PrintyGroup, slug=self.kwargs["printy_group"]
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
    template_name = "mainapp/item_details.html"
    home_path = settings.PRINTY_PATH
    home_label = settings.PRINTY_LABLE

    def get_object(self, queryset=None):
        return Printy.objects.get(
            slug=self.kwargs["printy_item"], published=True
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Запись выбранной оснастки в сессию."""
        self.request.session["printy_item"] = self.object.slug
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
