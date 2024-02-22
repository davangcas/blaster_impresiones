from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import activate
from simple_history.models import HistoricalRecords


class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name="roles")

    def get_permission_names(self):
        activate(settings.LANGUAGE_CODE)
        permission_names = ", ".join(
            [
                permission.name.replace("Can view", "Ver")
                .replace("Can add", "Agregar")
                .replace("Can change", "Editar")
                .replace("Can delete", "Eliminar")
                for permission in self.permissions.all()
            ]
        )
        return (
            f"{permission_names[:40]}(...)"
            if len(permission_names) > 20
            else permission_names
        )

    def __str__(self):
        return self.name


class User(AbstractUser):
    historical = HistoricalRecords()
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, related_name="users", null=True, blank=True
    )
