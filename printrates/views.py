from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, RedirectView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from printrates.forms import MonthlyCostForm, PrintRateForm, PrintRateVariablesForm
from printrates.models import MonthlyCost, PrintRate, PrintRateVariables
from printrates.serializers import (
    MonthlyCostSerializer,
    PrintRateSerializer,
    PrintRateVariablesSerializer,
)
from printrates.services import generate_print_rate


class PrintRateListView(PostListViewMixin):
    model = PrintRate
    template_name = "printrates/list.html"
    permission_required = "printrates.view_printrate"
    serializer_class = PrintRateSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Precio de impresión por hora"
        context["create_url"] = reverse_lazy("printrates:create")
        context["active_section"] = "configuration"
        return context


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


class PrintRateDeleteView(CustomAdminViewMixin, DeleteView):
    model = PrintRate
    template_name = "printrates/delete.html"
    success_url = reverse_lazy("printrates:list")
    permission_required = "printrates.delete_printrate"

    def get_success_url(self):
        messages.success(self.request, "Valor eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar valor de precio por hora"
        context["cancel_url"] = reverse_lazy("printrates:list")
        context["active_section"] = "configuration"
        return context


class MonthlyCostListView(PostListViewMixin):
    model = MonthlyCost
    template_name = "monthly_costs/list.html"
    permission_required = "printrates.view_monthlycost"
    serializer_class = MonthlyCostSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Costos mensuales"
        context["create_url"] = reverse_lazy("printrates:monthly_costs_create")
        context["active_section"] = "configuration"
        return context


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


class PrintRateVariablesListView(PostListViewMixin):
    model = PrintRateVariables
    template_name = "variables/list.html"
    permission_required = "printrates.view_printratevariables"
    serializer_class = PrintRateVariablesSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Variables a considerar en el precio de impresión"
        context["create_url"] = reverse_lazy("printrates:variables_create")
        context["active_section"] = "configuration"
        return context


class PrintRateVariablesCreateView(CustomAdminViewMixin, CreateView):
    model = PrintRateVariables
    template_name = "variables/create.html"
    success_url = reverse_lazy("printrates:list")
    form_class = PrintRateVariablesForm
    permission_required = "printrates.add_printratevariables"

    def form_valid(self, form):
        messages.success(self.request, "Variables creadas correctamente")
        return super().form_valid(form)

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


class PrintRateVariablesDeleteView(CustomAdminViewMixin, DeleteView):
    model = PrintRateVariables
    template_name = "variables/delete.html"
    success_url = reverse_lazy("printrates:list")
    permission_required = "printrates.delete_printratevariables"

    def get_success_url(self):
        messages.success(self.request, "Variables eliminadas correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar variables a considerar en el precio de impresión"
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
