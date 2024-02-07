from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from users.forms import CreateRoleForm, CreateUserForm, UpdateRoleForm, UpdateUserForm
from users.models import Role, User


class UserListView(ListView):
    model = User
    template_name = "users/list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("role")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Usuarios"
        context["create_url"] = reverse_lazy("users:create")
        context["active_section"] = "users"
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
        context["active_section"] = "users"
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
        context["active_section"] = "users"
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class RoleListView(ListView):
    model = Role
    template_name = "roles/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Roles"
        context["create_url"] = reverse_lazy("users:roles_create")
        context["active_section"] = "roles"
        return context


class RoleCreateView(CreateView):
    model = Role
    form_class = CreateRoleForm
    template_name = "roles/create.html"
    success_url = reverse_lazy("users:roles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context


class RoleUpdateView(UpdateView):
    model = Role
    form_class = UpdateRoleForm
    template_name = "roles/update.html"
    success_url = reverse_lazy("users:roles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context


class RoleDeleteView(DeleteView):
    model = Role
    template_name = "roles/delete.html"
    success_url = reverse_lazy("users:roles")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context
