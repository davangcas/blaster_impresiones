from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/product_form.html"
    fields = "__all__"
    success_url = reverse_lazy("products:list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/product_form.html"
    fields = "__all__"
    success_url = reverse_lazy("products:list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:list")
