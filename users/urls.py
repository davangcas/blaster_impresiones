from django.urls import path

from users.views import UserListView, UserCreateView, UserDeleteView, UserUpdateView

app_name = "users"
urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
]
