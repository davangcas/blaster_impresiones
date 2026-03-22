from django.urls import path

from orders.views import (
    OrderChangeStateRedirectView,
    OrderCreateView,
    OrderDatatableView,
    OrderDeleteMultipleView,
    OrderDeleteView,
    OrderItemCreateView,
    OrderItemDatatableView,
    OrderItemDeleteView,
    OrderItemListView,
    OrderItemUpdateView,
    OrderListView,
    OrderUpdateView,
    PrintOrderItemChangeColorFormView,
    PrintOrderItemChangeColorMultipleView,
    PrintOrderItemChangeStateFormView,
    PrintOrderItemChangeStateMultipleView,
    PrintOrderItemChangeStateView,
    PrintOrderItemDatatableView,
    PrintOrderItemDetailView,
    PrintOrderItemListView,
    PrintOrderItemModelsDatatableView,
    PrintOrderItemUpdateView,
)

app_name = "orders"
urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("json/", OrderDatatableView.as_view(), name="json"),
    path("create/", OrderCreateView.as_view(), name="create"),
    path("update/<int:pk>/", OrderUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete"),
    path("delete-multiple/", OrderDeleteMultipleView.as_view(), name="delete_multiple"),
    path("items/<int:pk>/", OrderItemListView.as_view(), name="items"),
    path("items/json/<int:pk>/", OrderItemDatatableView.as_view(), name="items_json"),
    path("items/create/<int:pk>/", OrderItemCreateView.as_view(), name="items_create"),
    path(
        "items/update/<int:pk>/",
        OrderItemUpdateView.as_view(),
        name="items_update",
    ),
    path(
        "items/delete/<int:pk>/",
        OrderItemDeleteView.as_view(),
        name="items_delete",
    ),
    path(
        "print_order_items/<int:pk>/",
        PrintOrderItemListView.as_view(),
        name="print_order_items",
    ),
    path(
        "print_order_items/json/<int:pk>/",
        PrintOrderItemDatatableView.as_view(),
        name="print_order_items_json",
    ),
    path(
        "print_order_items/update/<int:pk>/",
        PrintOrderItemUpdateView.as_view(),
        name="print_order_items_update",
    ),
    path(
        "print_order_items/change_state/<int:pk>/",
        PrintOrderItemChangeStateView.as_view(),
        name="print_order_items_change_state",
    ),
    path(
        "print_order_items/change-state-form/",
        PrintOrderItemChangeStateFormView.as_view(),
        name="print_order_items_change_state_form",
    ),
    path(
        "print_order_items/change-state-multiple/",
        PrintOrderItemChangeStateMultipleView.as_view(),
        name="print_order_items_change_state_multiple",
    ),
    path(
        "print_order_items/change-color-form/",
        PrintOrderItemChangeColorFormView.as_view(),
        name="print_order_items_change_color_form",
    ),
    path(
        "print_order_items/change-color-multiple/",
        PrintOrderItemChangeColorMultipleView.as_view(),
        name="print_order_items_change_color_multiple",
    ),
    path(
        "change-state/<int:pk>/",
        OrderChangeStateRedirectView.as_view(),
        name="change_state",
    ),
    path(
        "print_order_items/detail/<int:pk>/",
        PrintOrderItemDetailView.as_view(),
        name="print_order_items_detail",
    ),
    path(
        "print_order_items/models/json/<int:pk>/",
        PrintOrderItemModelsDatatableView.as_view(),
        name="print_order_items_models_json",
    ),
]
