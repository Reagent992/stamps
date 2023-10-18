from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.models import Stamp, StampGroup


class StampGroupView(TitleBreadcrumbsMixin, ListView):
    """Главная страница, группы печатей."""

    model = StampGroup
    queryset = StampGroup.objects.filter(published=True)
    template_name = "mainapp/index.html"
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.INDEX_TITLE
    crumbs = []

    def get_context_data(self, **kwargs):
        """Передаем название View в шаблон."""
        return {**super().get_context_data(**kwargs), "IndexView": True}


class GroupedStampsView(TitleBreadcrumbsMixin, ListView):
    """Печати отфильтрованные оп группе."""

    model = StampGroup
    template_name = "mainapp/index.html"
    paginate_by = settings.PAGINATION_AMOUNT

    def get_queryset(self):
        self.stamp_group = get_object_or_404(
            StampGroup, slug=self.kwargs["group"]
        )
        return Stamp.objects.filter(group=self.stamp_group, published=True)

    def get_title(self):
        """Заголовок вкладки."""
        return self.stamp_group.title

    def get_context_data(self, *, object_list=None, **kwargs):
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
    template_name = "mainapp/item_details.html"

    def get_object(self, queryset=None):
        return Stamp.objects.get(slug=self.kwargs["slug_item"], published=True)

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Запись выбранной печати в сессию."""
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
