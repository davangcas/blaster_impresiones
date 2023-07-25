from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo electrónico", blank=True, null=True)
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Número de teléfono"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
