from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from clients.forms import ClientCreateEditForm
from clients.models import Client
from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from core.services import get_select_checkbox


class ClientListView(CustomAdminViewMixin, TemplateView):
    model = Client
    template_name = "clients/list.html"
    permission_required = "clients.view_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        context["create_url"] = reverse_lazy("clients:create")
        context["active_section"] = "clients"
        context["json_view_url"] = reverse_lazy("clients:json")
        return context


class ClientDatatableView(CustomDatatablesJsonMixin):
    permission_required = "clients.view_client"
    model = Client
    columns = ["id", "first_name", "last_name", "email", "phone_number", "actions"]

    def render_column(self, row, column):
        if column == "id":
            return get_select_checkbox(row)
        if column == "email":
            return row.email or "No posee email registrado"
        if column == "actions":
            update_url = reverse_lazy("clients:update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("clients:delete", kwargs={"pk": row.id})
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class ClientCreateView(CustomAdminViewMixin, CreateView):
    model = Client
    template_name = "clients/create.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientCreateEditForm
    permission_required = "clients.add_client"

    def form_valid(self, form):
        messages.success(self.request, "Cliente creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el cliente")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context


class ClientUpdateView(CustomAdminViewMixin, UpdateView):
    model = Client
    template_name = "clients/update.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientCreateEditForm
    permission_required = "clients.change_client"

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el cliente")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context


class ClientDeleteView(CustomAdminViewMixin, DeleteView):
    model = Client
    template_name = "clients/delete.html"
    success_url = reverse_lazy("clients:list")
    permission_required = "clients.delete_client"

    def get_success_url(self):
        messages.success(self.request, "Cliente eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context
