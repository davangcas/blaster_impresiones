from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from financials.forms import TransactionCreateEditForm, TransactionCreateFromAccountForm
from financials.models import Account, Transaction
from financials.serializers import TransactionSerializer


class AccountDetailView(CustomAdminViewMixin, TemplateView):
    template_name = "financials/account.html"
    permission_required = "financials.view_account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cuenta Personal"
        context["active_section"] = "financials"
        context["account"] = Account.objects.get_or_create(
            user=self.request.user, name=self.request.user.username
        )[0]
        context["organization_account"] = Account.objects.get_or_create(
            user=None, name="blaster"
        )[0]
        return context


class TransactionListView(PostListViewMixin):
    template_name = "transactions/list.html"
    permission_required = "financials.view_transaction"
    model = Transaction
    serializer_class = TransactionSerializer

    def get_permission_required(self):
        permissions = super().get_permission_required()
        from_personal_account = self.request.GET.get("from_personal_account")

        if from_personal_account:
            permissions = [
                "financials.view_account",
            ]
        return permissions

    def get_queryset(self):
        queryset = super().get_queryset()
        from_personal_account = self.request.GET.get("from_personal_account")

        if from_personal_account:
            queryset = queryset.filter(
                from_account__user=self.request.user
            ) | queryset.filter(to_account__user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Transacciones"
        context["active_section"] = "transactions"
        context["create_url"] = reverse_lazy("financials:transactions_create")
        context["account"] = Account.objects.get_or_create(user=None, name="blaster")[0]
        return context


class TransactionCreateView(CustomAdminViewMixin, CreateView):
    model = Transaction
    template_name = "transactions/create.html"
    form_class = TransactionCreateEditForm
    permission_required = "financials.add_transaction"

    def get_permission_required(self):
        permissions = super().get_permission_required()

        if self.request.GET.get("from_personal_account"):
            permissions = ("financials.view_account",)

        return permissions

    def get_form_class(self):
        form_class = TransactionCreateEditForm

        if self.request.GET.get("from_personal_account"):
            form_class = TransactionCreateFromAccountForm

        return form_class

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        if self.request.GET.get("from_personal_account"):
            form_kwargs["user"] = self.request.user

        return form_kwargs

    def get_success_url(self):
        if self.request.GET.get("from_personal_account"):
            return reverse_lazy("financials:account")
        return reverse_lazy("financials:transactions")

    def form_valid(self, form):
        messages.success(self.request, "Transacción creada exitosamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la transacción")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nueva Transacción"
        context["cancel_url"] = (
            reverse_lazy("financials:account")
            if self.request.GET.get("from_personal_account")
            else reverse_lazy("financials:transactions")
        )
        context["active_section"] = (
            "financials"
            if self.request.GET.get("from_personal_account")
            else "transactions"
        )
        return context


class TransactionUpdateView(CustomAdminViewMixin, UpdateView):
    model = Transaction
    form_class = TransactionCreateEditForm
    template_name = "transactions/update.html"
    success_url = reverse_lazy("financials:transactions")
    permission_required = "financials.change_transaction"

    def form_valid(self, form):
        messages.success(self.request, "Transacción actualizada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la transacción")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar Transacción"
        context["cancel_url"] = reverse_lazy("financials:transactions")
        context["active_section"] = "transactions"
        return context


class TransactionDeleteView(CustomAdminViewMixin, DeleteView):
    model = Transaction
    template_name = "transactions/delete.html"
    success_url = reverse_lazy("financials:transactions")
    permission_required = "financials.delete_transaction"

    def get_success_url(self):
        messages.success(self.request, "Transacción eliminada correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar Transacción"
        context["cancel_url"] = reverse_lazy("financials:transactions")
        context["active_section"] = "transactions"
        return context
