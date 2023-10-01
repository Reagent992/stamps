from django.urls import path

from mainapp.views import GroupedStamps, Index, StampDetail

app_name = 'mainapp'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:group>/', GroupedStamps.as_view(), name='stamps'),
    path('<slug:group>/<slug:slug_item>/', StampDetail.as_view(),
         name='item_details'),
]
