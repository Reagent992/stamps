from django.urls import path

from mainapp.views import GroupedStampsView, StampDetailView, StampGroupView

app_name = 'mainapp'

urlpatterns = [
    path('', StampGroupView.as_view(), name='index'),
    path('<slug:group>/', GroupedStampsView.as_view(), name='stamps'),
    path('<slug:group>/<slug:slug_item>/', StampDetailView.as_view(),
         name='item_details'),
]
