from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from mainapp.models import Stamp, Group

User = get_user_model()


def get_paginated_page(request, queryset):
    """Пагинатор, выводит по 10 постов на странице."""
    paginator = Paginator(queryset, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Главная страница. Выводит список типов печатей(групп)."""
    groups = Group.objects.all()
    page_obj = get_paginated_page(request, groups)
    template = 'mainapp/index.html'

    context = {
        'title': 'Заголовок',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def stamps(request, slug):
    """Страница с печатями(после выбора группы)."""
    group = get_object_or_404(Group, slug=slug)
    all_stamps = Stamp.objects.filter(group=group)
    page_obj = get_paginated_page(request, all_stamps)
    template = 'mainapp/index.html'

    breadcrumbs = [
        {'title': 'Главная', 'url': '/'},
        {'title': group.title, 'url': f'/{group}/'},
    ]

    context = {
        'title': 'Заголовок',
        'page_obj': page_obj,
        'its_stamps': True,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, template, context)


def item_details(request, group, slug_item):
    """Подробности о товаре."""
    item = Stamp.objects.get(slug=slug_item)
    template = 'mainapp/item_details.html'
    group_obj = Group.objects.get(slug=group)

    breadcrumbs = [
        {'title': 'Главная', 'url': '/'},
        {'title': group_obj.title, 'url': f'/{group}/'},
        {'title': item.title, 'url': request.path},
    ]

    context = {
        'title': item.__str__(),
        'page_obj': item,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, template, context)
