from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.fields import CustomPriceDecimalField
from core.forms import DefaultModelForm
from users.models import Role, User


class CreateUserForm(DefaultModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "(opcional)"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "(opcional)"}
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False,
    )
    role = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                "class": "select2bs4 select2-hidden-accessible",
                "style": "width: 100%;",
            }
        ),
        label="Rol",
        required=True,
        queryset=Role.objects.all(),
    )
    salary = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Salario",
        required=True,
        max_digits=15,
        decimal_places=2,
        initial=0,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "salary",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].queryset = Role.objects.all()
        self.fields["role"].initial = Role.objects.first()
        self.fields["role"].label = "Rol"
        self.fields["role"].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password2")

        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UpdateUserForm(CreateUserForm):
    pass


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
