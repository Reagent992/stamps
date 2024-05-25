from django.urls import path

from orders.views import CreateStampOrderView, SuccessFormView

app_name = "orders"

urlpatterns = [
    path(
        "success/",
        SuccessFormView.as_view(),
        name="order_success",
    ),
    path(
        "<slug:group>/<slug:slug_item>/order",
        CreateStampOrderView.as_view(),
        name="create_order",
    ),
]
