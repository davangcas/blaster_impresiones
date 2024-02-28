from core.forms import DefaultModelForm
from products.models import Product
from django import forms
from core.fields import CustomPriceDecimalField


class ProductEditForm(DefaultModelForm):
    price = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Precio",
        required=True,
        max_digits=10,
        decimal_places=2,
        initial=0,
    )
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
        fields = ("name", "price", "link", "description", "image", "stock", "available")


class ProductCreateForm(ProductEditForm):
    pass
