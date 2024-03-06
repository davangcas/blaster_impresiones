from django.views.generic import ListView

from core.mixins import PostListViewMixin
from financials.models import Account, Transaction
from financials.serializers import TransactionSerializer


class TransactionListView(PostListViewMixin, ListView):
    template_name = "financials/account.html"
    permission_required = "financials.view_account"
    model = Transaction
    serializer_class = TransactionSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Transacciones"
        context["accounts"] = Account.objects.filter(users__isnull=True).distinct()
        context["active_section"] = "financials"
        return context
