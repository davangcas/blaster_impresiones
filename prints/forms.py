from typing import Any
from django import forms

from core.fields import CustomPriceDecimalField
from core.forms import DefaultModelForm
from prints.models import Print, PrintMaterial, PrintModel, PrintModelRelation


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


class PrintModelCommonForm(DefaultModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Cantidad",
        required=True,
        help_text="Cantidad de modelos de impresión",
        initial=1,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nombre"
        self.fields["x_scale"].label = "Escala X"
        self.fields["x_scale"].initial = 100
        self.fields["y_scale"].label = "Escala Y"
        self.fields["y_scale"].initial = 100
        self.fields["z_scale"].label = "Escala Z"
        self.fields["z_scale"].initial = 100
        self.fields["file"].label = "STL"

    class Meta:
        model = PrintModel
        fields = "__all__"


class PrintModelCreateForm(PrintModelCommonForm):
    def __init__(self, *args, **kwargs):
        self.print_id = kwargs.pop("print_id")
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        PrintModelRelation.objects.create(
            print_id=self.print_id,
            print_model_id=instance.id,
            quantity=self.cleaned_data["quantity"],
        )
        return instance


class PrintModelUpdateForm(PrintModelCommonForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].initial = self.instance.printmodelrelation_set.first().quantity

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        instance.printmodelrelation_set.update(quantity=self.cleaned_data["quantity"])
        return instance
