from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from printrates.forms import MonthlyCostForm, PrintRateForm, PrintRateVariablesForm
from printrates.models import MonthlyCost, PrintRate, PrintRateVariables
from printrates.services import generate_print_rate


class PrintRateListView(CustomAdminViewMixin, TemplateView):
    model = PrintRate
    template_name = "printrates/list.html"
    permission_required = "printrates.view_printrate"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        singleton = PrintRate.get_singleton()
        history = list(singleton.historical.all().order_by("-history_date"))

        current_printrate_price = singleton.rate
        previous_printrate_price = history[1].rate if len(history) > 1 else 0
        first_printrate_price = history[-1].rate if history else 0

        context["title"] = "Precios de impresión por hora - historial"
        context["current_printrate"] = current_printrate_price
        context["previous_printrate"] = previous_printrate_price
        context["first_printrate"] = first_printrate_price
        context["create_url"] = (
            None  # Singleton: no se agregan filas, solo se actualiza
        )
        context["active_section"] = "configuration"
        context["json_view_url"] = reverse_lazy("printrates:json")
        return context


class PrintRateDatatableView(CustomDatatablesJsonMixin):
    """Tabla con el historial del singleton (history records)."""

    permission_required = "printrates.view_printrate"
    model = PrintRate.historical.model
    columns = ["history_date", "rate"]

    def get_initial_queryset(self):
        singleton = PrintRate.get_singleton()
        return self.model.objects.filter(id=singleton.pk).order_by("-history_date")

    def render_column(self, row, column):
        if column == "history_date":
            return timezone.localtime(row.history_date).strftime("%d/%m/%Y %H:%M")
        if column == "rate":
            return f"${row.rate}"
        return super().render_column(row, column)


class PrintRateCreateView(CustomAdminViewMixin, CreateView):
    model = PrintRate
    template_name = "printrates/create.html"
    success_url = reverse_lazy("printrates:list")
    form_class = PrintRateForm
    permission_required = "printrates.add_printrate"

    def form_valid(self, form):
        messages.success(self.request, "Valor creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el valor")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear valor de precio por hora"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class PrintRateUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintRate
    template_name = "printrates/update.html"
    success_url = reverse_lazy("printrates:list")
    form_class = PrintRateForm
    permission_required = "printrates.change_printrate"

    def get_object(self, queryset=None):
        return PrintRate.get_singleton()

    def form_valid(self, form):
        messages.success(self.request, "Valor actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el valor")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar valor de precio por hora"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class MonthlyCostDatatableView(CustomDatatablesJsonMixin):
    permission_required = "printrates.view_monthlycost"
    model = MonthlyCost
    columns = ["name", "cost", "updated_at", "actions"]

    def render_column(self, row, column):
        if column == "updated_at":
            return timezone.localtime(row.updated_at).strftime("%d/%m/%Y %H:%M")
        if column == "cost":
            return f"${row.cost}"
        if column == "actions":
            update_url = reverse_lazy(
                "printrates:monthly_costs_update", kwargs={"pk": row.pk}
            )
            delete_url = reverse_lazy(
                "printrates:monthly_costs_delete", kwargs={"pk": row.pk}
            )
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class MonthlyCostCreateView(CustomAdminViewMixin, CreateView):
    model = MonthlyCost
    template_name = "monthly_costs/create.html"
    success_url = reverse_lazy("printrates:list")
    form_class = MonthlyCostForm
    permission_required = "printrates.add_monthlycost"

    def form_valid(self, form):
        messages.success(self.request, "Costo creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el costo")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear costo mensual"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class MonthlyCostUpdateView(CustomAdminViewMixin, UpdateView):
    model = MonthlyCost
    template_name = "monthly_costs/update.html"
    success_url = reverse_lazy("printrates:list")
    form_class = MonthlyCostForm
    permission_required = "printrates.change_monthlycost"

    def form_valid(self, form):
        messages.success(self.request, "Costo actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el costo")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar costo mensual"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class MonthlyCostDeleteView(CustomAdminViewMixin, DeleteView):
    model = MonthlyCost
    template_name = "monthly_costs/delete.html"
    success_url = reverse_lazy("printrates:list")
    permission_required = "printrates.delete_monthlycost"

    def get_success_url(self):
        messages.success(self.request, "Costo eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar costo mensual"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class PrintRateVariablesDatatableView(CustomDatatablesJsonMixin):
    permission_required = "printrates.view_printratevariables"
    model = PrintRateVariables
    columns = [
        "created_at",
        "failure_percentage",
        "maintenance_cost",
        "minutes_spent_per_print",
        "extra_percentage",
        "expected_daily_print_hours",
        "general_profit_margin",
        "actions",
    ]

    def get_initial_queryset(self):
        return self.model.objects.filter(pk=1).order_by("-created_at")

    def render_column(self, row, column):
        if column == "created_at":
            return timezone.localtime(row.created_at).strftime("%d/%m/%Y %H:%M")
        if column == "failure_percentage":
            return f"{row.failure_percentage}%"
        if column == "extra_percentage":
            return f"{row.extra_percentage}%"
        if column == "general_profit_margin":
            return f"{row.general_profit_margin}%"
        if column == "maintenance_cost":
            return f"${row.maintenance_cost}"
        if column == "actions":
            update_url = reverse_lazy(
                "printrates:variables_update", kwargs={"pk": row.pk}
            )
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
            """
        return super().render_column(row, column)


class PrintRateVariablesCreateView(CustomAdminViewMixin, CreateView):
    model = PrintRateVariables
    template_name = "variables/create.html"
    success_url = reverse_lazy("printrates:list")
    form_class = PrintRateVariablesForm
    permission_required = "printrates.add_printratevariables"

    def dispatch(self, request, *args, **kwargs):
        if PrintRateVariables.objects.filter(pk=1).exists():
            return redirect("printrates:variables_update", pk=1)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.pk = 1
        instance.save()
        messages.success(self.request, "Variables creadas correctamente")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear las variables")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear variables a considerar en el precio de impresión"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class PrintRateVariablesUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintRateVariables
    template_name = "variables/update.html"
    success_url = reverse_lazy("printrates:list")
    form_class = PrintRateVariablesForm
    permission_required = "printrates.change_printratevariables"

    def get_object(self, queryset=None):
        return PrintRateVariables.get_singleton()

    def form_valid(self, form):
        messages.success(self.request, "Variables actualizadas correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar las variables")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar variables a considerar en el precio de impresión"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class GenerateNewPrintRateView(CustomAdminViewMixin, RedirectView):
    pattern_name = "printrates:list"
    permission_required = "printrates.add_printrate"

    def get_redirect_url(self, *args, **kwargs):
        generate_print_rate()
        messages.success(
            self.request, "Nuevo valor de precio por hora generado correctamente"
        )
        return super().get_redirect_url(*args, **kwargs)
