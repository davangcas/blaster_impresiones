from django.urls import path

from prints.views import (
    PrintCreateView,
    PrintDeleteView,
    PrintListView,
    PrintMaterialCreateView,
    PrintMaterialDeleteView,
    PrintMaterialListView,
    PrintMaterialUpdateView,
    PrintUpdateView,
    PrintModelRelationListView,
    PrintModelCreateView,
    PrintModelUpdateView,
    PrintModelDeleteView,
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
        PrintModelRelationListView.as_view(),
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
]
