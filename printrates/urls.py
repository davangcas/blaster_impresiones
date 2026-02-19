from django.urls import path

from printrates.views import (
    GenerateNewPrintRateView,
    MonthlyCostCreateView,
    MonthlyCostDatatableView,
    MonthlyCostDeleteView,
    MonthlyCostUpdateView,
    PrintRateDatatableView,
    PrintRateListView,
    PrintRateUpdateView,
    PrintRateVariablesCreateView,
    PrintRateVariablesDatatableView,
    PrintRateVariablesUpdateView,
)

app_name = "printrates"
urlpatterns = [
    path("", PrintRateListView.as_view(), name="list"),
    path("json/", PrintRateDatatableView.as_view(), name="json"),
    path("update/", PrintRateUpdateView.as_view(), name="update"),
    path(
        "monthly-costs/json/",
        MonthlyCostDatatableView.as_view(),
        name="monthly_costs_json",
    ),
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
    path(
        "variables/json/",
        PrintRateVariablesDatatableView.as_view(),
        name="variables_json",
    ),
    path(
        "variables/create/",
        PrintRateVariablesCreateView.as_view(),
        name="variables_create",
    ),
    path(
        "variables/update/<int:pk>/",
        PrintRateVariablesUpdateView.as_view(),
        name="variables_update",
    ),
    path(
        "generate-new-rate/",
        GenerateNewPrintRateView.as_view(),
        name="generate_new_rate",
    ),
]
