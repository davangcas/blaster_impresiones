from django.db import models


class Print(models.Model):
    hours = models.PositiveSmallIntegerField()
    minutes = models.PositiveSmallIntegerField()
    grams = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)


class PrintModel(models.Model):
    name = models.CharField(max_length=150)
    x_scale = models.PositiveSmallIntegerField()
    y_scale = models.PositiveSmallIntegerField()
    z_scale = models.PositiveSmallIntegerField()


class PrintFile(models.Model):
    file = models.FileField(upload_to="print_model/")
    print_model = models.ForeignKey(PrintModel, on_delete=models.CASCADE)


class RelatedPrint(models.Model):
    print_model = models.ForeignKey(PrintModel, on_delete=models.CASCADE)
    print = models.ForeignKey(Print, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, blank=True)
