from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.stamps, name='stamps'),
    path('<slug:group>/<slug:slug_item>/', views.item_details,
         name='item_details'),
]
