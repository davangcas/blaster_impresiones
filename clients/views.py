from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from clients.forms import ClientCreateForm, ClientEditForm
from clients.models import Client


class ClientListView(ListView):
    model = Client
    template_name = "clients/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        context["create_url"] = reverse_lazy("clients:create")
        context["active_section"] = "clients"
        return context


class ClientCreateView(CreateView):
    model = Client
    template_name = "clients/create.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "clients/update.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/delete.html"
    success_url = reverse_lazy("clients:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar cliente"
        context["cancel_url"] = reverse_lazy("clients:list")
        context["active_section"] = "clients"
        return context
