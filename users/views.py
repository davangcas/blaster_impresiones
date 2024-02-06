from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from users.models import User
from users.forms import CreateUserForm, UpdateUserForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("role")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Usuarios"
        context["create_url"] = reverse_lazy("users:create")
        return context


class UserCreateView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        return context
