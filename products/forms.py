from core.forms import DefaultModelForm
from products.models import Product
from django import forms
from core.fields import CustomPriceDecimalField


class ProductEditForm(DefaultModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Nombre",
        required=True,
    )
    price = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Precio",
        required=True,
        max_digits=10,
        decimal_places=2,
        initial=0,
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        label="Descripción",
        required=True,
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="Imagen",
        required=False,
    )
    stock = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Stock",
        required=True,
        initial=0,
    )
    available = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Disponible",
        required=False,
        initial=True,
        help_text="Indica si el producto está disponible para la venta",
    )

    class Meta:
        model = Product
        fields = ("name", "price", "description", "image", "stock", "available")


class ProductCreateForm(ProductEditForm):
    pass
