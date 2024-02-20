from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from products.forms import ProductCreateForm, ProductEditForm
from products.models import Product
from products.serializers import ProductSerializer


class ProductListView(PostListViewMixin):
    model = Product
    template_name = "products/list.html"
    permission_required = "products.view_product"
    serializer_class = ProductSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        context["create_url"] = reverse_lazy("products:create")
        context["active_section"] = "products"
        return context


class ProductCreateView(CustomAdminViewMixin, CreateView):
    model = Product
    template_name = "products/create.html"
    success_url = reverse_lazy("products:list")
    form_class = ProductCreateForm
    permission_required = "products.add_product"

    def form_valid(self, form):
        messages.success(self.request, "Producto creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el producto")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear producto"
        context["cancel_url"] = reverse_lazy("products:list")
        context["active_section"] = "products"
        return context


class ProductUpdateView(CustomAdminViewMixin, UpdateView):
    model = Product
    template_name = "products/update.html"
    success_url = reverse_lazy("products:list")
    form_class = ProductEditForm
    permission_required = "products.change_product"

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el producto")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar producto"
        context["cancel_url"] = reverse_lazy("products:list")
        context["active_section"] = "products"
        return context


class ProductDeleteView(CustomAdminViewMixin, DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy("products:list")
    permission_required = "products.delete_product"

    def get_success_url(self):
        messages.success(self.request, "Producto eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar producto"
        context["cancel_url"] = reverse_lazy("products:list")
        context["active_section"] = "products"
        return context
