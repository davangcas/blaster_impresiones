from django import forms
from django.contrib.auth.models import Permission

from core.forms import DefaultModelForm
from users.models import Role, User


class CreateUserForm(DefaultModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
        )


class UpdateUserForm(DefaultModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
        )


class CreateRoleForm(DefaultModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nombre",
        required=True,
        help_text="Nombre del rol",
    )
    permissions = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                "class": "select2bs4 select2-hidden-accessible select-all",
                "style": "width: 100%;",
            }
        ),
        label="Permisos",
        required=False,
        help_text="Permisos que posee el rol",
        queryset=Permission.objects.all(),
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "permissions",
        )


class UpdateRoleForm(CreateRoleForm):

    class Meta:
        model = Role
        fields = (
            "name",
            "permissions",
        )
