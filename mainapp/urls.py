from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:group>/', views.GroupedStamps.as_view(), name='stamps'),
    path('<slug:group>/<slug:slug_item>/', views.StampDetail.as_view(),
         name='item_details'),
]
