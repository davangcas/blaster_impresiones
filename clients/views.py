from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from clients.forms import ClientCreateForm, ClientEditForm
from clients.models import Client
from core.mixins import CustomAdminViewMixin, PostListViewMixin
from clients.serializers import ClientSerializer


class ClientListView(PostListViewMixin):
    model = Client
    template_name = "clients/list.html"
    permission_required = "clients.view_client"
    serializer_class = ClientSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        context["create_url"] = reverse_lazy("clients:create")
        context["active_section"] = "clients"
        return context


class ClientCreateView(CustomAdminViewMixin, CreateView):
    model = Client
    template_name = "clients/create.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientCreateForm
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
    form_class = ClientEditForm
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
