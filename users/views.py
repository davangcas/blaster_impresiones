from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.mixins import CustomAdminViewMixin
from users.forms import CreateRoleForm, CreateUserForm, UpdateRoleForm, UpdateUserForm
from users.models import Role, User


class UserListView(CustomAdminViewMixin, ListView):
    model = User
    template_name = "users/list.html"
    permission_required = "users.view_user"

    def get_queryset(self):
        return super().get_queryset().select_related("role")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Usuarios"
        context["create_url"] = reverse_lazy("users:create")
        context["active_section"] = "users"
        return context


class UserCreateView(CustomAdminViewMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.add_user"

    def get_success_url(self):
        messages.success(self.request, "Usuario creado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class UserUpdateView(CustomAdminViewMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.change_user"

    def get_success_url(self):
        messages.success(self.request, "Usuario actualizado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class UserDeleteView(CustomAdminViewMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.delete_user"

    def get_success_url(self):
        messages.success(self.request, "Usuario eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class RoleListView(CustomAdminViewMixin, ListView):
    model = Role
    template_name = "roles/list.html"
    permission_required = "users.view_role"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Roles"
        context["create_url"] = reverse_lazy("users:roles_create")
        context["active_section"] = "roles"
        return context


class RoleCreateView(CustomAdminViewMixin, CreateView):
    model = Role
    form_class = CreateRoleForm
    template_name = "roles/create.html"
    success_url = reverse_lazy("users:roles")
    permission_required = "users.add_role"

    def get_success_url(self):
        messages.success(self.request, "Rol creado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context


class RoleUpdateView(CustomAdminViewMixin, UpdateView):
    model = Role
    form_class = UpdateRoleForm
    template_name = "roles/update.html"
    success_url = reverse_lazy("users:roles")
    permission_required = "users.change_role"

    def get_success_url(self):
        messages.success(self.request, "Rol actualizado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context


class RoleDeleteView(CustomAdminViewMixin, DeleteView):
    model = Role
    template_name = "roles/delete.html"
    success_url = reverse_lazy("users:roles")
    permission_required = "users.delete_role"

    def get_success_url(self):
        messages.success(self.request, "Rol eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context
