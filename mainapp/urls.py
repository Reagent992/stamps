from django.urls import path

from mainapp.views import (
    CreateStampOrderView,
    GroupedStampsView,
    StampDetailView,
    StampGroupView,
    SuccessFormView,
)

app_name = "mainapp"

urlpatterns = [
    path(
        "",
        StampGroupView.as_view(),
        name="index",
    ),
    path(
        "success/",
        SuccessFormView.as_view(),
        name="order_success",
    ),
    path(
        "<slug:group>/",
        GroupedStampsView.as_view(),
        name="stamps",
    ),
    path(
        "<slug:group>/<slug:slug_item>/",
        StampDetailView.as_view(),
        name="item_details",
    ),
    path(
        "<slug:group>/<slug:slug_item>/order",
        CreateStampOrderView.as_view(),
        name="stamp_form",
    ),
]
