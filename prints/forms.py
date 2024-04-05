from django import forms

from core.fields import CustomPriceDecimalField
from core.forms import DefaultModelForm
from prints.models import (
    Print,
    PrintMaterial,
    PrintMaterialColor,
    PrintModel,
    PrintModelRelation,
)


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
        widget=forms.Select(
            attrs={
                "class": "select2bs4 select2-hidden-accessible",
                "style": "width: 100%;",
            }
        ),
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
        self.fields["layer_height"].label = "Altura de capa"
        self.fields["layer_height"].help_text = "Altura de capa en milímetros"
        self.fields["infill"].label = "Relleno"
        self.fields["infill"].help_text = "Porcentaje de relleno"
        self.fields["nozzle"].label = "Diámetro de boquilla"
        self.fields["nozzle"].help_text = "Diámetro de la boquilla en milímetros"
        self.fields["speed"].label = "Velocidad de impresión"
        self.fields["speed"].help_text = "Velocidad de impresión en mm/s"

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
        model_instance = PrintModel.objects.create(
            name="Único",
            x_scale=100,
            y_scale=100,
            z_scale=100,
        )
        PrintModelRelation.objects.create(
            print_model=model_instance,
            print=instance,
            quantity=1
        )
        return instance


class PrintModelCommonForm(DefaultModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Cantidad",
        required=True,
        help_text="Cantidad de veces que el modelo esta presente en la impresión",
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
        self.fields["quantity"].initial = (
            self.instance.printmodelrelation_set.first().quantity
        )

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        instance.printmodelrelation_set.update(quantity=self.cleaned_data["quantity"])
        return instance


class PrintMaterialColorUpdateForm(DefaultModelForm):
    def __init__(self, *args, **kwargs):
        self.material_id = kwargs.pop("material_id")
        super().__init__(*args, **kwargs)
        self.fields["color"].label = "Color"
        self.fields["remaining"].label = "Cantidad"
        self.fields["remaining"].help_text = (
            "Cantidad de material de impresión expresado en gramos"
        )
        self.fields["remaining"].initial = 1000
        self.fields["remaining"].widget.attrs["min"] = 0

    class Meta:
        model = PrintMaterialColor
        exclude = ("material",)

    def clean_color(self):
        color = self.cleaned_data["color"]
        material = PrintMaterial.objects.get(id=self.material_id)
        filter_lookup = {"material": material, "color": color}
        exclude_lookup = {}

        if self.instance:
            exclude_lookup = {"id": self.instance.id}

        if (
            PrintMaterialColor.objects.filter(**filter_lookup)
            .exclude(**exclude_lookup)
            .exists()
        ):
            raise forms.ValidationError(
                f"El color ya existe para el material {material.name}"
            )

        return color


class PrintMaterialColorCreateForm(PrintMaterialColorUpdateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"].initial = "Blanco"

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.material_id = self.material_id
        instance.save()
        return instance
