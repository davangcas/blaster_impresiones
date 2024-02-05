from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from clients.forms import ClientCreateForm, ClientEditForm
from clients.models import Client


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    template_name = "clients/list.html"


class ClientCreateView(CreateView):
    model = Client
    template_name = "clients/create.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientCreateForm


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "clients/update.html"
    success_url = reverse_lazy("clients:list")
    form_class = ClientEditForm


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/delete.html"
    success_url = reverse_lazy("clients:list")
