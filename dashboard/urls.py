from django.contrib.auth.views import LogoutView
from django.urls import path

from dashboard.views import IndexView, LoginFormView

app_name = "dashboard"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="dashboard:login"), name="logout"),
]
