from django.urls import path

from products.views import (
    ExtraProductCostCreateView,
    ExtraProductCostDatatableView,
    ExtraProductCostDeleteView,
    ExtraProductCostListView,
    ExtraProductCostUpdateView,
    ProductCreateView,
    ProductDatatableView,
    ProductDeleteView,
    ProductListView,
    ProductUpdateView,
)

app_name = "products"
urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("json/", ProductDatatableView.as_view(), name="json"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete"),
    path(
        "extra-costs/<int:pk>/", ExtraProductCostListView.as_view(), name="extra_costs"
    ),
    path(
        "extra-costs/json/<int:pk>/",
        ExtraProductCostDatatableView.as_view(),
        name="extra_costs_json",
    ),
    path(
        "extra-costs/create/<int:pk>/",
        ExtraProductCostCreateView.as_view(),
        name="extra_costs_create",
    ),
    path(
        "extra-costs/update/<int:pk>/",
        ExtraProductCostUpdateView.as_view(),
        name="extra_costs_update",
    ),
    path(
        "extra-costs/delete/<int:pk>/",
        ExtraProductCostDeleteView.as_view(),
        name="extra_costs_delete",
    ),
]
