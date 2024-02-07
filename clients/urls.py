from django.urls import path

from . import views

app_name = "clients"
urlpatterns = [
    path("", views.ClientListView.as_view(), name="list"),
    path("create/", views.ClientCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ClientUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.ClientDeleteView.as_view(), name="delete"),
]
