from core.forms import DefaultModelForm
from products.models import Product, ExtraProductCost
from django import forms
from core.fields import CustomPriceDecimalField


class ProductEditForm(DefaultModelForm):
    available = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Disponible",
        required=False,
        initial=True,
        help_text="Indica si el producto está disponible para la venta",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["image"].label = "Imagen"
        self.fields["stock"].initial = 0
        self.fields["description"].label = "Descripción"
        self.fields["name"].label = "Nombre"
        self.fields["link"].label = "Enlace"
        self.fields["link"].required = False
        self.fields["link"].help_text = "Enlace a la página de los modelos del producto"
        self.fields["link"].widget.attrs["placeholder"] = "(opcional)"

    class Meta:
        model = Product
        fields = ("name", "link", "description", "image", "stock", "available")


class ProductCreateForm(ProductEditForm):
    pass

class ExtraProductCostUpdateForm(DefaultModelForm):
    cost = CustomPriceDecimalField(
        label="Costo",
        help_text="Costo adicional del producto",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = ExtraProductCost
        fields = ("name", "description", "cost")
        labels = {
            "name": "Nombre",
            "description": "Descripción",
        }


class ExtraProductCostCreateForm(ExtraProductCostUpdateForm):
    def __init__(self, *args, **kwargs):
        self.product_id = kwargs.pop("product_id")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.product_id = self.product_id
        if commit:
            instance.save()
        return instance
