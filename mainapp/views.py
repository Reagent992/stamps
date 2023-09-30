from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from core.mixins import PageTitleViewMixin
from mainapp.models import Group, Stamp

User = get_user_model()


class Index(PageTitleViewMixin, ListView):
    """Главная страница, группы печатей."""

    queryset = Group.objects.filter(published=True)
    template_name = 'mainapp/index.html'
    paginate_by = settings.PAGINATION_AMOUNT
    title = settings.INDEX_TITLE


class GroupedStamps(PageTitleViewMixin, ListView):
    """Печати отфильтрованные оп группе."""

    template_name = 'mainapp/index.html'
    paginate_by = settings.PAGINATION_AMOUNT

    def get_queryset(self):
        self.group = get_object_or_404(Group, slug=self.kwargs['group'])
        return Stamp.objects.filter(group=self.group)

    def get_title(self):
        return self.group.title

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slug': self.group,
            'its_stamps': True,
        })
        return context


class StampDetail(PageTitleViewMixin, DetailView):
    """Подробности о печати."""

    template_name = 'mainapp/item_details.html'
    context_object_name = 'page_obj'

    def get_object(self, queryset=None):
        self.item = Stamp.objects.get(slug=self.kwargs['slug_item'])
        return self.item

    def get_title(self):
        return self.item.__str__()
