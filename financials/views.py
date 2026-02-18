from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from core.services import get_select_checkbox
from financials.choices import ACCOUNT_TYPES
from financials.forms import TransactionCreateEditForm, TransactionCreateFromAccountForm
from financials.models import Account, Transaction


class AccountDetailView(CustomAdminViewMixin, TemplateView):
    template_name = "financials/account.html"
    permission_required = "financials.view_account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cuenta Personal"
        context["active_section"] = "financials"
        context["account"] = Account.objects.get_or_create(
            user=self.request.user,
            name=self.request.user.username,
            account_type=ACCOUNT_TYPES[1][0],
        )[0]
        context["organization_account"] = Account.objects.get_or_create(
            user=None, name="blaster", account_type=ACCOUNT_TYPES[0][0]
        )[0]
        return context


class TransactionListView(CustomAdminViewMixin, TemplateView):
    template_name = "transactions/list.html"
    permission_required = "financials.view_transaction"
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Transacciones"
        context["active_section"] = "transactions"
        context["create_url"] = reverse_lazy("financials:transactions_create")
        context["account"] = Account.objects.get_or_create(user=None, name="blaster")[0]
        context["json_view_url"] = reverse_lazy("financials:transactions_json")
        return context


class TransactionDatatableView(CustomDatatablesJsonMixin):
    permission_required = "financials.view_transaction"
    model = Transaction

    def get_columns(self):
        from_personal_account = self.request.GET.get("from_personal_account")
        table_columns = [
            "id",
            "date",
            "description",
            "amount",
            "from_account.name",
            "to_account.name",
            "actions",
        ]

        if from_personal_account:
            table_columns.remove("actions")

        return table_columns

    def get_initial_queryset(self):
        initial_queryset = super().get_initial_queryset()
        from_personal_account = self.request.GET.get("from_personal_account")

        if from_personal_account:
            initial_queryset = initial_queryset.filter(
                from_account__user=self.request.user
            ) | initial_queryset.filter(to_account__user=self.request.user)

        return initial_queryset

    def get_permission_required(self):
        permissions = super().get_permission_required()
        from_personal_account = self.request.GET.get("from_personal_account")

        if from_personal_account:
            permissions = [
                "financials.view_account",
            ]
        return permissions

    def render_column(self, row, column):
        if column == "id":
            if self.request.GET.get("from_personal_account"):
                return ""
            return get_select_checkbox(row)
        if column == "date":
            return timezone.localtime(row.date).strftime("%d/%m/%Y %H:%M")
        if column == "from_account.name":
            return row.from_account.name if row.from_account else "Fuentes Externas"
        if column == "to_account.name":
            return row.to_account.name if row.to_account else "Fuentes Externas"
        if column == "amount":
            return f"${row.amount}"
        if column == "actions":
            delete_url = reverse_lazy(
                "financials:transactions_delete", kwargs={"pk": row.id}
            )
            return f"""
                <a href="{delete_url}" class="btn btn-danger m-1">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


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
