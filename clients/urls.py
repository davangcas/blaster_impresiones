from django.urls import path

from clients.views import (
    ClientCreateView,
    ClientDatatableView,
    ClientDeleteView,
    ClientListView,
    ClientUpdateView,
)

app_name = "clients"
urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("json/", ClientDatatableView.as_view(), name="json"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete"),
]
