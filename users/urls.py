from django.urls import path

from users.views import (
    ChangeDarkModeView,
    ChangePasswordView,
    RoleCreateView,
    RoleDatatableView,
    RoleDeleteMultipleView,
    RoleDeleteView,
    RoleListView,
    RoleUpdateView,
    UserCreateView,
    UserDatatableView,
    UserDeleteMultipleView,
    UserDeleteView,
    UserListView,
    UserUpdateView,
)

app_name = "users"
urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("json/", UserDatatableView.as_view(), name="json"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete-multiple/", UserDeleteMultipleView.as_view(), name="delete_multiple"),
    path("roles/", RoleListView.as_view(), name="roles"),
    path("roles/json/", RoleDatatableView.as_view(), name="roles_json"),
    path("roles/create/", RoleCreateView.as_view(), name="roles_create"),
    path("roles/delete/<int:pk>/", RoleDeleteView.as_view(), name="roles_delete"),
    path(
        "roles/delete-multiple/",
        RoleDeleteMultipleView.as_view(),
        name="roles_delete_multiple",
    ),
    path("roles/update/<int:pk>/", RoleUpdateView.as_view(), name="roles_update"),
    path("change_dark_mode/", ChangeDarkModeView.as_view(), name="change_dark_mode"),
]
