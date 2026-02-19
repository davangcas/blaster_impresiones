from decimal import Decimal

from django.db import models
from simple_history.models import HistoricalRecords


class PrintRate(models.Model):
    """Singleton: solo existe una instancia (id=1) con el precio actual. El historial se guarda en history."""

    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    historical = HistoricalRecords()

    def __str__(self):
        return f"{self.rate}"

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def get_singleton(cls):
        """Devuelve la única instancia del modelo (singleton). La crea si no existe."""
        instance, _ = cls.objects.get_or_create(
            pk=1,
            defaults={"rate": Decimal("0.00")},
        )
        return instance


class MonthlyCost(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cost}"

    class Meta:
        ordering = ["-created_at"]


class PrintRateVariables(models.Model):
    """Singleton: solo existe una instancia (id=1) con las variables actuales."""

    failure_percentage = models.PositiveSmallIntegerField(default=0)
    maintenance_cost = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00
    )
    minutes_spent_per_print = models.PositiveSmallIntegerField(default=0)
    extra_percentage = models.PositiveSmallIntegerField(default=0)
    available_printers = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def get_singleton(cls):
        """Devuelve la única instancia del modelo (singleton). La crea si no existe."""
        instance, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                "failure_percentage": 0,
                "maintenance_cost": Decimal("0.00"),
                "minutes_spent_per_print": 0,
                "extra_percentage": 0,
                "available_printers": 1,
            },
        )
        return instance
