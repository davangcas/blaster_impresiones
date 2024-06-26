from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from users.forms import ChangePasswordForm, CreateEditRoleForm, CreateEditUserForm
from users.models import Role, User


class UserListView(CustomAdminViewMixin, TemplateView):
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
        context["json_view_url"] = reverse_lazy("users:json")
        return context


class UserDatatableView(CustomDatatablesJsonMixin):
    permission_required = "users.view_user"
    model = User
    columns = ["username", "email", "first_name", "last_name", "role.name", "actions"]

    def render_column(self, row, column):
        if column == "actions":
            update_url = reverse_lazy("users:update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("users:delete", kwargs={"pk": row.id})
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class UserCreateView(CustomAdminViewMixin, CreateView):
    model = User
    form_class = CreateEditUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.add_user"

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el usuario")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear usuario"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class UserUpdateView(CustomAdminViewMixin, UpdateView):
    model = User
    form_class = CreateEditUserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.change_user"

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el usuario")
        return super().form_invalid(form)

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


class ChangePasswordView(CustomAdminViewMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy("users:list")
    permission_required = "users.change_user"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Contraseña actualizada correctamente")
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la contraseña")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cambiar contraseña"
        context["cancel_url"] = reverse_lazy("users:list")
        context["active_section"] = "users"
        return context


class RoleListView(CustomAdminViewMixin, TemplateView):
    model = Role
    template_name = "roles/list.html"
    permission_required = "users.view_role"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Roles"
        context["create_url"] = reverse_lazy("users:roles_create")
        context["active_section"] = "roles"
        context["json_view_url"] = reverse_lazy("users:roles_json")
        return context


class RoleDatatableView(CustomDatatablesJsonMixin):
    permission_required = "users.view_role"
    model = Role
    columns = ["name", "permissions__name", "actions"]

    def render_column(self, row, column):
        if column == "permissions__name":
            return row.get_permission_names()
        if column == "actions":
            update_url = reverse_lazy("users:roles_update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("users:roles_delete", kwargs={"pk": row.id})
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class RoleCreateView(CustomAdminViewMixin, CreateView):
    model = Role
    form_class = CreateEditRoleForm
    template_name = "roles/create.html"
    success_url = reverse_lazy("users:roles")
    permission_required = "users.add_role"

    def form_valid(self, form):
        messages.success(self.request, "Rol creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el rol")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear rol"
        context["cancel_url"] = reverse_lazy("users:roles")
        context["active_section"] = "roles"
        return context


class RoleUpdateView(CustomAdminViewMixin, UpdateView):
    model = Role
    form_class = CreateEditRoleForm
    template_name = "roles/update.html"
    success_url = reverse_lazy("users:roles")
    permission_required = "users.change_role"

    def form_valid(self, form):
        messages.success(self.request, "Rol actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el rol")
        return super().form_invalid(form)

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


class ChangeDarkModeView(RedirectView):
    url = reverse_lazy("dashboard:index")

    def get(self, request, *args, **kwargs):
        request.user.admin_dark_mode = not request.user.admin_dark_mode
        request.user.save()
        messages.success(request, "Modo actualizado correctamente")
        return super().get(request, *args, **kwargs)
