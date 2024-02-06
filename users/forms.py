from core.forms import DefaultModelForm
from users.models import User


class CreateUserForm(DefaultModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
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
            "is_active",
        )
