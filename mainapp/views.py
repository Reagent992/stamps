from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView

from core.mixins import TitleBreadcrumbsMixin
from mainapp.models import Group, Stamp


class Index(TitleBreadcrumbsMixin, ListView):
    """Главная страница, группы печатей."""
    model = Group
    queryset = Group.objects.filter(published=True)
    template_name = 'mainapp/index.html'
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.INDEX_TITLE
    crumbs = []


class GroupedStamps(TitleBreadcrumbsMixin, ListView):
    """Печати отфильтрованные оп группе."""

    model = Group
    template_name = 'mainapp/index.html'
    paginate_by = settings.PAGINATION_AMOUNT

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        return [(self.group.title, reverse_lazy('mainapp:stamps'))]

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['group'])
        return Stamp.objects.filter(group=self.group)

    def get_title(self):
        """Заголовок вкладки."""
        return self.group.title

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slug': self.group,
            'its_stamps': True,
        })
        return context


class StampDetail(TitleBreadcrumbsMixin, DetailView):
    """Подробности о печати."""

    model = Stamp
    template_name = 'mainapp/item_details.html'
    context_object_name = 'page_obj'

    @cached_property
    def crumbs(self):
        """Breadcrumbs."""
        self.group = get_object_or_404(Group, slug=self.kwargs['group'])
        return [
            (self.group.title,
             reverse_lazy('mainapp:stamps', kwargs={
                 'group': self.kwargs['group']})),
            (self.item.title,
             reverse_lazy('mainapp:item_details'))]

    def get_object(self, queryset=None):
        self.item = Stamp.objects.get(slug=self.kwargs['slug_item'])
        return self.item

    def get_title(self):
        """Заголовок вкладки."""
        return self.item.__str__()
