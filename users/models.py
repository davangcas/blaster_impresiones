from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from simple_history.models import HistoricalRecords


class Role(models.Model):
    name = models.CharField(max_length=100)
    historical = HistoricalRecords()
    permissions = models.ManyToManyField(Permission, related_name="roles")


class User(AbstractUser):
    historical = HistoricalRecords()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name="users")

    def save(self, *args, **kwargs):
        self.user_permissions.clear()
        self.user_permissions.add(*self.role.permissions.all())
        return super().save(*args, **kwargs)
