from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from products.forms import (
    ExtraProductCostCreateForm,
    ExtraProductCostUpdateForm,
    ProductCreateEditForm,
)
from products.models import ExtraProductCost, Product
from products.serializers import ExtraProductCostSerializer, ProductSerializer


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
    form_class = ProductCreateEditForm
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
    form_class = ProductCreateEditForm
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


class ExtraProductCostListView(PostListViewMixin):
    model = ExtraProductCost
    template_name = "extra_costs/list.html"
    permission_required = "products.view_extraproductcost"
    serializer_class = ExtraProductCostSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Costos adicionales"
        context["create_url"] = reverse_lazy("products:extra_costs_create")
        context["active_section"] = "products"
        return context


class ExtraProductCostCreateView(CustomAdminViewMixin, CreateView):
    model = ExtraProductCost
    template_name = "extra_costs/create.html"
    form_class = ExtraProductCostCreateForm
    permission_required = "products.add_extraproductcost"

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["product_id"] = self.kwargs.get("pk")
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy("prints:list", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        messages.success(self.request, "Costo adicional creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el costo adicional")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear costo adicional"
        context["cancel_url"] = reverse_lazy(
            "prints:list", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        return context


class ExtraProductCostUpdateView(CustomAdminViewMixin, UpdateView):
    model = ExtraProductCost
    template_name = "extra_costs/update.html"
    form_class = ExtraProductCostUpdateForm
    permission_required = "products.change_extraproductcost"

    def get_success_url(self):
        return reverse_lazy("prints:list", kwargs={"pk": self.get_object().product_id})

    def form_valid(self, form):
        messages.success(self.request, "Costo adicional actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el costo adicional")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar costo adicional"
        context["cancel_url"] = reverse_lazy(
            "prints:list", kwargs={"pk": self.get_object().product_id}
        )
        context["active_section"] = "products"
        return context


class ExtraProductCostDeleteView(CustomAdminViewMixin, DeleteView):
    model = ExtraProductCost
    template_name = "extra_costs/delete.html"
    permission_required = "products.delete_extraproductcost"

    def get_success_url(self):
        messages.success(self.request, "Costo adicional eliminado correctamente")
        return reverse_lazy("prints:list", kwargs={"pk": self.get_object().product_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar costo adicional"
        context["cancel_url"] = reverse_lazy(
            "prints:list", kwargs={"pk": self.get_object().product_id}
        )
        context["active_section"] = "products"
        return context
