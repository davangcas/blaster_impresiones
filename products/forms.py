from django import forms

from core.fields import CustomPriceDecimalField
from core.forms import DefaultModelForm
from products.models import ExtraProductCost, Product, Category


class ProductCreateEditForm(DefaultModelForm):
    categories = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                "class": "select2bs4 select2-hidden-accessible select-all",
                "style": "width: 100%;",
                "data-placeholder": "(Opcional)",
            }
        ),
        label="Categorias",
        required=False,
        queryset=Category.objects.all(),
    )

    available = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Disponible",
        required=False,
        initial=False,
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
        self.fields["link"].required = True
        self.fields["link"].help_text = "Enlace a la página de los modelos del producto"

    class Meta:
        model = Product
        fields = ("name", "link", "description", "categories", "image", "stock", "available")

    def clean_available(self):
        available = self.cleaned_data["available"]
        if available and not self.cleaned_data.get("image"):
            raise forms.ValidationError(
                "Para marcar un producto como disponible, debe tener una imagen asociada."
            )
        return available


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


class CategoryCreateEditForm(DefaultModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")
        labels = {
            "name": "Nombre",
            "description": "Descripción",
        }
