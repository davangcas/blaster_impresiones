from django.urls import path

from landing.views import IndexView, AboutView

app_name = "landing"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
]
