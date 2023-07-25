from django.urls import path

from clients.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
)


app_name = "clients"
urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="delete"),
]
