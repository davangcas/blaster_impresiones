from core.forms import DefaultModelForm
from printrates.models import MonthlyCost, PrintRate
from django import forms
from core.fields import CustomPriceDecimalField


class PrintRateForm(DefaultModelForm):
    rate = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Precio por hora",
        required=True,
        max_digits=15,
        decimal_places=2,
        initial=0,
        help_text="Precio por hora de impresión",
    )
    class Meta:
        model = PrintRate
        fields = ["rate"]


class MonthlyCostForm(DefaultModelForm):
    cost = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Monto",
        required=True,
        max_digits=15,
        decimal_places=2,
        initial=0,
        help_text="Monto mensual a pagar",
    )

    class Meta:
        model = MonthlyCost
        fields = ["name", "description", "cost"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nombre"
        self.fields["description"].label = "Descripción"
