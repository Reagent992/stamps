from django.urls import path

from printy.views import (
    PrintyDetailView,
    PrintyGroupContentView,
    PrintyGroupsView,
)

app_name = "printy"

urlpatterns = [
    path("", PrintyGroupsView.as_view(), name="printy_index"),
    path(
        "<slug:printy_group>/",
        PrintyGroupContentView.as_view(),
        name="printys",
    ),
    path(
        "<slug:printy_group>/<slug:printy_item>/",
        PrintyDetailView.as_view(),
        name="printy_details",
    ),
]
