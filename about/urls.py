from django.urls import path

from . import views

app_name = "about"

urlpatterns = [
    path("contacts/", views.ContactView.as_view(), name="contacts"),
]
