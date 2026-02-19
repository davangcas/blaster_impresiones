from django.urls import path

from products.views import (
    CategoryCreateView,
    CategoryDatatableView,
    CategoryDeleteMultipleView,
    CategoryDeleteView,
    CategoryGetOptionsView,
    CategoryListView,
    CategoryUpdateView,
    ExtraProductCostCreateView,
    ExtraProductCostDatatableView,
    ExtraProductCostDeleteView,
    ExtraProductCostListView,
    ExtraProductCostUpdateView,
    ProductCreateView,
    ProductDatatableView,
    ProductDeleteMultipleView,
    ProductDeleteView,
    ProductImageCreateView,
    ProductImageDatatableView,
    ProductImageDeleteView,
    ProductImageUpdateView,
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
        "delete-multiple/", ProductDeleteMultipleView.as_view(), name="delete_multiple"
    ),
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
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("categories/json/", CategoryDatatableView.as_view(), name="categories_json"),
    path("categories/create/", CategoryCreateView.as_view(), name="categories_create"),
    path(
        "categories/update/<int:pk>/",
        CategoryUpdateView.as_view(),
        name="categories_update",
    ),
    path(
        "categories/delete/<int:pk>/",
        CategoryDeleteView.as_view(),
        name="categories_delete",
    ),
    path(
        "categories/delete-multiple/",
        CategoryDeleteMultipleView.as_view(),
        name="categories_delete_multiple",
    ),
    path(
        "categories/options/",
        CategoryGetOptionsView.as_view(),
        name="categories_options",
    ),
    path(
        "images/json/<int:pk>/",
        ProductImageDatatableView.as_view(),
        name="images_json",
    ),
    path(
        "images/create/<int:pk>/",
        ProductImageCreateView.as_view(),
        name="images_create",
    ),
    path(
        "images/update/<int:pk>/",
        ProductImageUpdateView.as_view(),
        name="images_update",
    ),
    path(
        "images/delete/<int:pk>/",
        ProductImageDeleteView.as_view(),
        name="images_delete",
    ),
]
