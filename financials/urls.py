from django.urls import path

from financials.views import TransactionListView

app_name = "financials"
urlpatterns = [
    path("account/", TransactionListView.as_view(), name="account"),
]
