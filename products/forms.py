from core.forms import DefaultModelForm
from products.models import Product


class ProductEditForm(DefaultModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "image", "stock", "available")


class ProductCreateForm(DefaultModelForm):
    class Meta:
        model = Product
        fields = ("name", "price", "description", "image", "stock", "available")
