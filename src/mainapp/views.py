from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.models import Stamp, StampGroup


class StampGroupView(TitleBreadcrumbsMixin, ListView):
    """Главная страница, группы печатей."""

    model = StampGroup
    queryset = StampGroup.filter_published.all()
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
            StampGroup.filter_published.all(), slug=self.kwargs["group"]
        )
        return Stamp.filter_published.filter(group=self.stamp_group)

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
            Stamp.filter_published.all(), slug=self.kwargs["slug_item"]
        )

    def get_title(self):
        """Заголовок вкладки."""
        return self.object.title

    def get_context_data(self, **kwargs):
        """Передача данных в шаблон."""
        return {
            **super().get_context_data(**kwargs),
            "printy_selected": bool(
                self.request.session.get(settings.USER_CHOICE_PRINTY_ID)
            ),
            "button_text": settings.BUTTON_CHOICE_PRINTY,
        }

    def post(self, request, *args, **kwargs):
        """Запись выбранной печати в сессию и редирект на выбор оснастки."""
        if "chosen_item_id" in request.POST:
            chosen_item_id = request.POST["chosen_item_id"]
            self.request.session[
                settings.USER_CHOICE_STAMP_ID
            ] = chosen_item_id
            return redirect(
                reverse("printy:printy_index")
                + f"?{settings.STAMP_ID_QUERY_PARAM}={chosen_item_id}"
            )
        return super().post(request, *args, **kwargs)

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        current_stamp_group = get_object_or_404(
            StampGroup.filter_published.all(), slug=self.kwargs["group"]
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
