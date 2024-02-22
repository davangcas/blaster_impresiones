from django.db import models
from products.models import Product


class PrintModel(models.Model):
    name = models.CharField(max_length=150)
    x_scale = models.PositiveSmallIntegerField()
    y_scale = models.PositiveSmallIntegerField()
    z_scale = models.PositiveSmallIntegerField()
    file = models.FileField(upload_to="print_model/", blank=True, null=True)

    def __str__(self):
        return self.name


class PrintMaterial(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return self.name


class Print(models.Model):
    material = models.ForeignKey(PrintMaterial, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    hours = models.PositiveSmallIntegerField()
    minutes = models.PositiveSmallIntegerField()
    grams = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    g_code = models.FileField(upload_to="print_gcode/", blank=True, null=True)

    def __str__(self):
        return f"{self.hours}h {self.minutes}m"


class PrintProduct(models.Model):
    print_model = models.ForeignKey(
        PrintModel, on_delete=models.CASCADE, blank=True, null=True
    )
    print = models.ForeignKey(Print, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, blank=True,)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["print_model", "print"], name="unique_print_model_print"
            )
        ]
