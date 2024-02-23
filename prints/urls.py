from django.urls import path

from prints.views import (
    PrintCreateView,
    PrintDeleteView,
    PrintListView,
    PrintMaterialColorCreateView,
    PrintMaterialColorDeleteView,
    PrintMaterialColorListView,
    PrintMaterialColorUpdateView,
    PrintMaterialCreateView,
    PrintMaterialDeleteView,
    PrintMaterialListView,
    PrintMaterialUpdateView,
    PrintModelCreateView,
    PrintModelDeleteView,
    PrintModelListView,
    PrintModelUpdateView,
    PrintUpdateView,
)

app_name = "prints"
urlpatterns = [
    path("materials/", PrintMaterialListView.as_view(), name="materials"),
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
    path("product-detail/<int:pk>/", PrintListView.as_view(), name="list"),
    path("product-detail/<int:pk>/create/", PrintCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", PrintDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", PrintUpdateView.as_view(), name="update"),
    path(
        "models-relation/<int:pk>/",
        PrintModelListView.as_view(),
        name="models",
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
