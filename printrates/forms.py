from django import forms

from core.fields import CustomPercentageField, CustomPriceDecimalField
from core.forms import DefaultModelForm
from printrates.models import MonthlyCost, PrintRate, PrintRateVariables


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
        self.fields["description"].required = False


class PrintRateVariablesForm(DefaultModelForm):
    failure_percentage = CustomPercentageField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Porcentaje de fallo",
        required=True,
        initial=0,
        help_text="Porcentaje de fallo de impresión",
    )
    maintenance_cost = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Costo de mantenimiento",
        required=True,
        max_digits=15,
        decimal_places=2,
        initial=0,
        help_text="Costo de mantenimiento de impresora",
    )
    minutes_spent_per_print = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Minutos por impresión",
        required=True,
        initial=0,
        help_text="Minutos promedio por impresión para mantenimiento de impresora",
    )
    extra_percentage = CustomPercentageField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Porcentaje extra",
        required=True,
        initial=0,
        help_text="Contingencia sobre el costo (antes del margen de ganancia)",
    )
    expected_daily_print_hours = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Horas de impresión esperadas por día",
        required=True,
        initial=6,
        min_value=1,
        help_text=(
            "Promedio diario de impresión. Se multiplica por 30 para repartir "
            "costos mensuales y sueldos sobre cada hora de impresión."
        ),
    )
    general_profit_margin = CustomPercentageField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Margen de ganancia general",
        required=True,
        initial=50,
        help_text="Porcentaje de ganancia sobre el costo total de cada impresión",
    )

    class Meta:
        model = PrintRateVariables
        fields = [
            "failure_percentage",
            "maintenance_cost",
            "minutes_spent_per_print",
            "extra_percentage",
            "expected_daily_print_hours",
            "general_profit_margin",
        ]
