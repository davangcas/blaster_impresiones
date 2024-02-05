from products.models import Product
from core.forms import DefaultModelForm


class ProductEditForm(DefaultModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "image", "stock", "available")


class ProductCreateForm(DefaultModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "image", "stock", "available")
