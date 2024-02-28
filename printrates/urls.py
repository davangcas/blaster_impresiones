from django.urls import path

from printrates.views import (
    PrintRateListView,
    PrintRateCreateView,
    PrintRateUpdateView,
    PrintRateDeleteView,
    MonthlyCostListView,
    MonthlyCostCreateView,
    MonthlyCostUpdateView,
    MonthlyCostDeleteView,
)


app_name = "printrates"
urlpatterns = [
    path("", PrintRateListView.as_view(), name="list"),
    path("create/", PrintRateCreateView.as_view(), name="create"),
    path("update/<int:pk>/", PrintRateUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", PrintRateDeleteView.as_view(), name="delete"),
    path("monthly-costs/", MonthlyCostListView.as_view(), name="monthly_costs"),
    path(
        "monthly-costs/create/",
        MonthlyCostCreateView.as_view(),
        name="monthly_costs_create",
    ),
    path(
        "monthly-costs/update/<int:pk>/",
        MonthlyCostUpdateView.as_view(),
        name="monthly_costs_update",
    ),
    path(
        "monthly-costs/delete/<int:pk>/",
        MonthlyCostDeleteView.as_view(),
        name="monthly_costs_delete",
    ),
]
