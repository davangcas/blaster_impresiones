from django.urls import path

from financials.views import (
    AccountDetailView,
    TransactionCreateView,
    TransactionDatatableView,
    TransactionDeleteView,
    TransactionListView,
    TransactionUpdateView,
)

app_name = "financials"
urlpatterns = [
    path("account/", AccountDetailView.as_view(), name="account"),
    path("transactions/", TransactionListView.as_view(), name="transactions"),
    path(
        "transactions/json/",
        TransactionDatatableView.as_view(),
        name="transactions_json",
    ),
    path(
        "transactions/create/",
        TransactionCreateView.as_view(),
        name="transactions_create",
    ),
    path(
        "transactions/update/<int:pk>/",
        TransactionUpdateView.as_view(),
        name="transactions_update",
    ),
    path(
        "transactions/delete/<int:pk>/",
        TransactionDeleteView.as_view(),
        name="transactions_delete",
    ),
]
