from django.conf import settings
from django.shortcuts import get_object_or_404
from view_breadcrumbs import BaseBreadcrumbMixin

from mainapp.models import Stamp
from printy.models import Printy


class PageTitleViewMixin:
    """Миксин для удобного назначения title"""

    title = ""

    def get_title(self):
        """
        Return the class title attr by default,
        but you can override this method to further customize
        """
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        if not title:
            raise ValueError("Заголовок(title) страницы не должен быть пустым")
        context["title"] = title
        return context


class TitleBreadcrumbsMixin(PageTitleViewMixin, BaseBreadcrumbMixin):
    """Обеднение миксинов для title и Breadcrumbs"""

    pass


class ItemsFromSessionMixin:
    """Get selected stamp and printy from session."""

    @property
    def selected_stamp(self) -> Stamp:
        return get_object_or_404(
            Stamp.filter_published.all(),
            id=self.request.session.get(settings.USER_CHOICE_STAMP_ID),
        )

    @property
    def selected_printy(self) -> Printy:
        return get_object_or_404(
            Printy.filter_published.all(),
            id=self.request.session.get(settings.USER_CHOICE_PRINTY_ID),
        )
