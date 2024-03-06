from django.urls import path

from products.views import (
    ExtraProductCostCreateView,
    ExtraProductCostDeleteView,
    ExtraProductCostListView,
    ExtraProductCostUpdateView,
    ProductCreateView,
    ProductDeleteView,
    ProductListView,
    ProductUpdateView,
)

app_name = "products"
urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="delete"),
    path(
        "extra-costs/<int:pk>/", ExtraProductCostListView.as_view(), name="extra_costs"
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
