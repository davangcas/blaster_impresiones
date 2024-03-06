from django.urls import path

from users.views import (
    RoleCreateView,
    RoleDeleteView,
    RoleListView,
    RoleUpdateView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

app_name = "users"
urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("roles/", RoleListView.as_view(), name="roles"),
    path("roles/create/", RoleCreateView.as_view(), name="roles_create"),
    path("roles/delete/<int:pk>/", RoleDeleteView.as_view(), name="roles_delete"),
    path("roles/update/<int:pk>/", RoleUpdateView.as_view(), name="roles_update"),
]
