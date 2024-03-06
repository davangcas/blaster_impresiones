from django.db import models


class PrintRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rate}"

    class Meta:
        ordering = ["-created_at"]


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
        return self.created_at

    class Meta:
        ordering = ["-created_at"]
