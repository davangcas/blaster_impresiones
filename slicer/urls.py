from django.urls import path

from slicer.views import PrintEstimateView

app_name = "slicer"

urlpatterns = [
    path("estimate/", PrintEstimateView.as_view(), name="estimate"),
]
