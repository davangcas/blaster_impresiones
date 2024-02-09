from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginFormView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="dashboard:login"), name="logout"),
]
