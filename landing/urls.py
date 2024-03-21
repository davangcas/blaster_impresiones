from django.urls import path

from landing.views import (
    AboutView,
    IndexView,
    ModelingServiceView,
    PrintServiceView,
    TermsAndConditionsView,
)

app_name = "landing"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("print-service/", PrintServiceView.as_view(), name="print_service"),
    path("modeling-service/", ModelingServiceView.as_view(), name="modeling_service"),
    path(
        "terms-and-conditions/",
        TermsAndConditionsView.as_view(),
        name="terms_and_conditions",
    ),
]
