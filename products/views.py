from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from products.forms import (
    ExtraProductCostCreateForm,
    ExtraProductCostUpdateForm,
    ProductCreateEditForm,
)
from products.models import ExtraProductCost, Product


class ProductListView(CustomAdminViewMixin, TemplateView):
    model = Product
    template_name = "products/list.html"
    permission_required = "products.view_product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Productos"
        context["create_url"] = reverse_lazy("products:create")
        context["active_section"] = "products"
        context["json_view_url"] = reverse_lazy("products:json")
        return context


class ProductDatatableView(CustomDatatablesJsonMixin):
    permission_required = "products.view_product"
    model = Product
    columns = ["id", "name", "price", "stock", "actions"]

    def render_column(self, row, column):
        if column == "price":
            return f"${row.price}"
        if column == "actions":
            update_url = reverse_lazy("products:update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("products:delete", kwargs={"pk": row.id})
            detail_url = reverse_lazy("prints:list", kwargs={"pk": row.id})
            return f"""
                <a href="{detail_url}" class="btn btn-info">
                    <i class="fas fa-eye"></i>
                </a>
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class ProductCreateView(CustomAdminViewMixin, CreateView):
    model = Product
    template_name = "products/create.html"
    success_url = reverse_lazy("products:list")
    form_class = ProductCreateEditForm
    permission_required = "products.add_product"

    def get_success_url(self):
        return reverse_lazy("prints:list", kwargs={"pk": self.object.pk})

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


class ExtraProductCostListView(CustomAdminViewMixin, TemplateView):
    model = ExtraProductCost
    template_name = "extra_costs/list.html"
    permission_required = "products.view_extraproductcost"

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Costos adicionales"
        context["create_url"] = reverse_lazy("products:extra_costs_create")
        context["active_section"] = "products"
        return context


class ExtraProductCostDatatableView(CustomDatatablesJsonMixin):
    permission_required = "products.view_extraproductcost"
    model = ExtraProductCost
    columns = ["name", "cost", "description", "actions"]

    def get_initial_queryset(self):
        return super().get_initial_queryset().filter(product_id=self.kwargs.get("pk"))

    def render_column(self, row, column):
        if column == "cost":
            return f"${row.cost}"
        if column == "actions":
            update_url = reverse_lazy(
                "products:extra_costs_update", kwargs={"pk": row.id}
            )
            delete_url = reverse_lazy(
                "products:extra_costs_delete", kwargs={"pk": row.id}
            )

            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


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
