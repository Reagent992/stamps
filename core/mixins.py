from view_breadcrumbs import BaseBreadcrumbMixin


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
