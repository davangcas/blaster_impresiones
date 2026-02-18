from django.contrib import messages
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import CharField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from core.services import get_select_checkbox
from prints.forms import (
    PrintCreateForm,
    PrintMaterialColorCreateForm,
    PrintMaterialColorUpdateForm,
    PrintMaterialForm,
    PrintModelCreateForm,
    PrintModelUpdateForm,
    PrintUpdateForm,
)
from prints.models import (
    Print,
    PrintMaterial,
    PrintMaterialColor,
    PrintModel,
    PrintModelRelation,
)
from products.models import Product


class PrintMaterialListView(CustomAdminViewMixin, TemplateView):
    model = PrintMaterial
    template_name = "materials/list.html"
    permission_required = "prints.view_printmaterial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Materiales de impresión"
        context["create_url"] = reverse_lazy("prints:materials_create")
        context["active_section"] = "materials"
        context["json_view_url"] = reverse_lazy("prints:materials_json")
        return context


class PrintMaterialDatatableView(CustomDatatablesJsonMixin):
    permission_required = "prints.view_printmaterial"
    model = PrintMaterial
    columns = ["id", "name", "price", "actions"]

    def render_column(self, row, column):
        if column == "id":
            return get_select_checkbox(row)
        if column == "price":
            return f"${row.price}"
        if column == "actions":
            colors_url = reverse_lazy("prints:colors", kwargs={"pk": row.id})
            update_url = reverse_lazy("prints:materials_update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("prints:materials_delete", kwargs={"pk": row.id})
            return f"""
                <a href="{colors_url}" class="btn btn-primary">
                    <i class="fas fa-tint"></i>
                </a>
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class PrintMaterialCreateView(CustomAdminViewMixin, CreateView):
    model = PrintMaterial
    form_class = PrintMaterialForm
    template_name = "materials/create.html"
    success_url = reverse_lazy("prints:materials")
    permission_required = "prints.add_printmaterial"

    def form_valid(self, form):
        messages.success(self.request, "Material de impresión creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el material de impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear material de impresión"
        context["cancel_url"] = reverse_lazy("prints:materials")
        context["active_section"] = "materials"
        return context


class PrintMaterialUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintMaterial
    form_class = PrintMaterialForm
    template_name = "materials/update.html"
    success_url = reverse_lazy("prints:materials")
    permission_required = "prints.change_printmaterial"

    def form_valid(self, form):
        messages.success(
            self.request, "Material de impresión actualizado correctamente"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el material de impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar material de impresión"
        context["cancel_url"] = reverse_lazy("prints:materials")
        context["active_section"] = "materials"
        return context


class PrintMaterialDeleteView(CustomAdminViewMixin, DeleteView):
    model = PrintMaterial
    template_name = "materials/delete.html"
    success_url = reverse_lazy("prints:materials")
    permission_required = "prints.delete_printmaterial"

    def get_success_url(self):
        messages.success(self.request, "Material de impresión eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar material de impresión"
        context["cancel_url"] = reverse_lazy("prints:materials")
        context["active_section"] = "materials"
        return context


class PrintListView(CustomAdminViewMixin, TemplateView):
    model = Print
    template_name = "prints/list.html"
    permission_required = "prints.view_print"

    def get_queryset(self):
        return Print.objects.filter(product__id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs.get("pk"))
        context["product"] = product
        context["title"] = "Impresiones necesarias"
        context["create_url"] = reverse_lazy(
            "prints:create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        context["json_view_url"] = reverse_lazy(
            "prints:json", kwargs={"pk": product.id}
        )
        return context


class PrintDatatableView(CustomDatatablesJsonMixin):
    permission_required = "prints.view_print"
    model = Print
    columns = [
        "id",
        "hours",
        "minutes",
        "grams",
        "material.name",
        "available_colors",
        "price",
        "actions",
    ]

    def get_initial_queryset(self):
        queryset = (
            super().get_initial_queryset().filter(product__id=self.kwargs.get("pk"))
        )

        available_colors_subquery = (
            PrintMaterialColor.objects.filter(
                material=OuterRef("material"), remaining__gte=OuterRef("grams")
            )
            .values("material")
            .annotate(color_list=StringAgg("color", delimiter=", "))
            .values("color_list")
        )

        queryset = queryset.annotate(
            available_colors=Coalesce(
                Subquery(available_colors_subquery, output_field=CharField()),
                Value("Sin color disponible"),
                output_field=CharField(),
            )
        )
        return queryset

    def render_column(self, row, column):
        if column == "id":
            return get_select_checkbox(row)
        if column == "price":
            return f"${row.price}"
        if column == "actions":
            g_code_content = ""
            detail_url = reverse_lazy("prints:models", kwargs={"pk": row.id})
            update_url = reverse_lazy("prints:update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("prints:delete", kwargs={"pk": row.id})

            if row.g_code:
                g_code_content = f"""
                    <a href="{row.g_code.url}" target="_blank" class="btn btn-primary">
                        <i class="fas fa-download"></i>
                    </a>
                """

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
                {g_code_content}
            """
        return super().render_column(row, column)


class PrintCreateView(CustomAdminViewMixin, CreateView):
    model = Print
    template_name = "prints/create.html"
    permission_required = "prints.add_print"
    form_class = PrintCreateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["product_id"] = self.kwargs.get("pk")
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy("prints:list", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        messages.success(self.request, "Impresión creada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:list", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        return context


class PrintUpdateView(CustomAdminViewMixin, UpdateView):
    model = Print
    template_name = "prints/update.html"
    permission_required = "prints.change_print"
    form_class = PrintUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "prints:list",
            kwargs={"pk": self.get_object().product.id},
        )

    def form_valid(self, form):
        messages.success(self.request, "Impresión actualizada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:list",
            kwargs={"pk": self.get_object().product.id},
        )
        context["active_section"] = "products"
        return context


class PrintDeleteView(CustomAdminViewMixin, DeleteView):
    model = Print
    template_name = "prints/delete.html"
    permission_required = "prints.delete_print"

    def get_success_url(self):
        messages.success(self.request, "Impresión eliminada correctamente")
        return reverse_lazy(
            "prints:list",
            kwargs={"pk": self.get_object().product.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:list",
            kwargs={"pk": self.get_object().product.id},
        )
        context["active_section"] = "products"
        return context


class PrintModelListView(CustomAdminViewMixin, DetailView):
    model = Print
    template_name = "models/list.html"
    permission_required = "prints.view_printmodelrelation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modelos de la impresión"
        context["create_url"] = reverse_lazy(
            "prints:models_create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        context["json_view_url"] = reverse_lazy(
            "prints:models_json", kwargs={"pk": self.kwargs.get("pk")}
        )
        return context


class PrintModelRelationDatatableView(CustomDatatablesJsonMixin):
    permission_required = "prints.view_printmodelrelation"
    model = PrintModelRelation
    columns = [
        "print_model.name",
        "print_model.x_scale",
        "print_model.y_scale",
        "print_model.z_scale",
        "quantity",
        "actions",
    ]

    def get_initial_queryset(self):
        return (
            super()
            .get_initial_queryset()
            .select_related("print_model")
            .filter(print__id=self.kwargs.get("pk"))
        )

    def render_column(self, row, column):
        if column == "actions":
            model_filte_content = ""
            update_url = reverse_lazy(
                "prints:models_update", kwargs={"pk": row.print_model.id}
            )
            delete_url = reverse_lazy(
                "prints:models_delete", kwargs={"pk": row.print_model.id}
            )

            if row.print_model.file:
                model_filte_content = f"""
                    <a href="{row.print_model.file.url}" target="_blank" class="btn btn-primary">
                        <i class="fas fa-download"></i>
                    </a>
                """

            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
                {model_filte_content}
            """
        return super().render_column(row, column)


class PrintModelCreateView(CustomAdminViewMixin, CreateView):
    model = PrintModel
    template_name = "models/create.html"
    permission_required = "prints.add_printmodel"
    form_class = PrintModelCreateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["print_id"] = self.kwargs.get("pk")
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy("prints:models", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        messages.success(self.request, "Modelo de impresión creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el modelo de impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear modelo de impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:models", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        return context


class PrintModelUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintModel
    template_name = "models/update.html"
    permission_required = "prints.change_printmodel"
    form_class = PrintModelUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "prints:models",
            kwargs={"pk": self.get_object().printmodelrelation_set.first().print.id},
        )

    def form_valid(self, form):
        messages.success(self.request, "Modelo de impresión actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el modelo de impresión")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar modelo de impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:models",
            kwargs={"pk": self.get_object().printmodelrelation_set.first().print.id},
        )
        context["active_section"] = "products"
        return context


class PrintModelDeleteView(CustomAdminViewMixin, DeleteView):
    model = PrintModel
    template_name = "models/delete.html"
    permission_required = "prints.delete_printmodel"

    def get_success_url(self):
        messages.success(self.request, "Modelo de impresión eliminado correctamente")
        return reverse_lazy(
            "prints:models",
            kwargs={"pk": self.get_object().printmodelrelation_set.first().print.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar modelo de impresión"
        context["cancel_url"] = reverse_lazy(
            "prints:models",
            kwargs={"pk": self.get_object().printmodelrelation_set.first().print.id},
        )
        context["active_section"] = "products"
        return context


class PrintMaterialColorListView(CustomAdminViewMixin, DetailView):
    model = PrintMaterial
    template_name = "colors/list.html"
    permission_required = "prints.view_printmaterialcolor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        context["title"] = f"Colores disponibles - {instance.name}"
        context["create_url"] = reverse_lazy(
            "prints:colors_create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "materials"
        context["json_view_url"] = reverse_lazy(
            "prints:colors_json", kwargs={"pk": instance.id}
        )
        return context


class PrintMaterialColorDatatableView(CustomDatatablesJsonMixin):
    permission_required = "prints.view_printmaterialcolor"
    model = PrintMaterialColor
    columns = ["color", "remaining", "actions"]

    def get_initial_queryset(self):
        return super().get_initial_queryset().filter(material__id=self.kwargs.get("pk"))

    def render_column(self, row, column):
        if column == "actions":
            update_url = reverse_lazy("prints:colors_update", kwargs={"pk": row.id})
            delete_url = reverse_lazy("prints:colors_delete", kwargs={"pk": row.id})
            return f"""
                <a href="{update_url}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                </a>
                <a href="{delete_url}" class="btn btn-danger">
                    <i class="fas fa-trash"></i>
                </a>
            """
        return super().render_column(row, column)


class PrintMaterialColorCreateView(CustomAdminViewMixin, CreateView):
    model = PrintMaterialColor
    template_name = "colors/create.html"
    permission_required = "prints.add_printmaterialcolor"
    form_class = PrintMaterialColorCreateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["material_id"] = self.kwargs.get("pk")
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy("prints:colors", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        messages.success(self.request, "Color del material creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el color del material")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear color del material"
        context["cancel_url"] = reverse_lazy(
            "prints:colors", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "materials"
        return context


class PrintMaterialColorUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintMaterialColor
    template_name = "colors/update.html"
    permission_required = "prints.change_printmaterialcolor"
    form_class = PrintMaterialColorUpdateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["material_id"] = self.get_object().material.id
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy(
            "prints:colors",
            kwargs={"pk": self.get_object().material.id},
        )

    def form_valid(self, form):
        messages.success(self.request, "Color del material actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el color del material")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar color del material"
        context["cancel_url"] = reverse_lazy(
            "prints:colors",
            kwargs={"pk": self.get_object().material.id},
        )
        context["active_section"] = "materials"
        return context


class PrintMaterialColorDeleteView(CustomAdminViewMixin, DeleteView):
    model = PrintMaterialColor
    template_name = "colors/delete.html"
    permission_required = "prints.delete_printmaterialcolor"

    def get_success_url(self):
        messages.success(self.request, "Color del material eliminado correctamente")
        return reverse_lazy(
            "prints:colors",
            kwargs={"pk": self.get_object().material.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar color del material"
        context["cancel_url"] = reverse_lazy(
            "prints:colors",
            kwargs={"pk": self.get_object().material.id},
        )
        context["active_section"] = "materials"
        return context
