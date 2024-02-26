from django.urls import path

from orders.views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView

app_name = "orders"
urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("create/", OrderCreateView.as_view(), name="create"),
    path("update/<int:pk>/", OrderUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete"),
]
