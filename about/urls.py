from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('contacts/', views.Contacts.as_view(), name='contacts'),
]
