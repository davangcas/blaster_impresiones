from django.urls import path

from prints.views import (
    PrintCreateView,
    PrintDatatableView,
    PrintDeleteView,
    PrintListView,
    PrintMaterialColorCreateView,
    PrintMaterialColorDatatableView,
    PrintMaterialColorDeleteView,
    PrintMaterialColorListView,
    PrintMaterialColorUpdateView,
    PrintMaterialCreateView,
    PrintMaterialDatatableView,
    PrintMaterialDeleteMultipleView,
    PrintMaterialDeleteView,
    PrintMaterialListView,
    PrintMaterialUpdateView,
    PrintModelCreateView,
    PrintModelDeleteView,
    PrintModelListView,
    PrintModelRelationDatatableView,
    PrintModelUpdateView,
    PrintUpdateView,
)

app_name = "prints"
urlpatterns = [
    path("materials/", PrintMaterialListView.as_view(), name="materials"),
    path(
        "materials/json/",
        PrintMaterialDatatableView.as_view(),
        name="materials_json",
    ),
    path(
        "materials/create/", PrintMaterialCreateView.as_view(), name="materials_create"
    ),
    path(
        "materials/update/<int:pk>/",
        PrintMaterialUpdateView.as_view(),
        name="materials_update",
    ),
    path(
        "materials/delete/<int:pk>/",
        PrintMaterialDeleteView.as_view(),
        name="materials_delete",
    ),
    path(
        "materials/delete-multiple/",
        PrintMaterialDeleteMultipleView.as_view(),
        name="materials_delete_multiple",
    ),
    path("product-detail/<int:pk>/", PrintListView.as_view(), name="list"),
    path("product-detail/json/<int:pk>/", PrintDatatableView.as_view(), name="json"),
    path("product-detail/<int:pk>/create/", PrintCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", PrintDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", PrintUpdateView.as_view(), name="update"),
    path(
        "models-relation/<int:pk>/",
        PrintModelListView.as_view(),
        name="models",
    ),
    path(
        "models-relation/json/<int:pk>/",
        PrintModelRelationDatatableView.as_view(),
        name="models_json",
    ),
    path(
        "models/create/<int:pk>/",
        PrintModelCreateView.as_view(),
        name="models_create",
    ),
    path(
        "models/update/<int:pk>/",
        PrintModelUpdateView.as_view(),
        name="models_update",
    ),
    path(
        "models/delete/<int:pk>/",
        PrintModelDeleteView.as_view(),
        name="models_delete",
    ),
    path("colors/<int:pk>/", PrintMaterialColorListView.as_view(), name="colors"),
    path(
        "colors/json/<int:pk>/",
        PrintMaterialColorDatatableView.as_view(),
        name="colors_json",
    ),
    path(
        "colors/create/<int:pk>/",
        PrintMaterialColorCreateView.as_view(),
        name="colors_create",
    ),
    path(
        "colors/update/<int:pk>/",
        PrintMaterialColorUpdateView.as_view(),
        name="colors_update",
    ),
    path(
        "colors/delete/<int:pk>/",
        PrintMaterialColorDeleteView.as_view(),
        name="colors_delete",
    ),
]
