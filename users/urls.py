from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.UserListView.as_view(), name="list"),
    path("create/", views.UserCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", views.UserDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", views.UserUpdateView.as_view(), name="update"),
    path("roles/", views.RoleListView.as_view(), name="roles"),
    path("roles/create/", views.RoleCreateView.as_view(), name="roles_create"),
    path("roles/delete/<int:pk>/", views.RoleDeleteView.as_view(), name="roles_delete"),
    path("roles/update/<int:pk>/", views.RoleUpdateView.as_view(), name="roles_update"),
]
