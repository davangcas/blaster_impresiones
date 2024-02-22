from prints.models import PrintMaterial, Print, PrintProduct
from core.forms import DefaultModelForm
from django import forms
from core.fields import CustomPriceDecimalField


class PrintMaterialForm(DefaultModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nombre",
        required=True,
        help_text="Nombre del material de impresión",
    )
    price = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Precio",
        required=True,
        max_digits=10,
        decimal_places=2,
        initial=0,
        help_text="Precio por kilogramo",
    )

    class Meta:
        model = PrintMaterial
        fields = "__all__"


class PrintUpdateForm(DefaultModelForm):
    material = forms.ModelChoiceField(
        queryset=PrintMaterial.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Material",
        required=True,
        help_text="Material de impresión",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["material"].empty_label = "Seleccione un material"
        self.fields["hours"].label = "Horas"
        self.fields["minutes"].label = "Minutos"
        self.fields["grams"].label = "Gramos"

    class Meta:
        model = Print
        exclude = ("product", "price")


class PrintCreateForm(PrintUpdateForm):
    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop("product_id")
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.product_id = self.product_id
        instance.save()
        return instance
