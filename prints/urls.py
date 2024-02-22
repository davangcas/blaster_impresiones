from django.urls import path

from prints.views import (
    PrintProductListView,
    PrintMaterialListView,
    PrintMaterialCreateView,
    PrintMaterialUpdateView,
    PrintMaterialDeleteView,
    PrintCreateView,
    PrintDeleteView,
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
    path("product-detail/<int:pk>/", PrintProductListView.as_view(), name="list"),
    path("product-detail/<int:pk>/create/", PrintCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", PrintDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", PrintUpdateView.as_view(), name="update"),
]
