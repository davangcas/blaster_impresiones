from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from prints.forms import (
    PrintCreateForm,
    PrintMaterialForm,
    PrintUpdateForm,
    PrintModelCreateForm,
    PrintModelUpdateForm,
)
from prints.models import Print, PrintMaterial, PrintModelRelation, PrintModel
from prints.serializers import (
    PrintMaterialSerializer,
    PrintSerializer,
    PrintModelRelationSerializer,
)
from products.models import Product


class PrintMaterialListView(PostListViewMixin):
    model = PrintMaterial
    template_name = "materials/list.html"
    permission_required = "prints.view_printmaterial"
    serializer_class = PrintMaterialSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Materiales de impresión"
        context["create_url"] = reverse_lazy("prints:materials_create")
        context["active_section"] = "materials"
        return context


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


class PrintListView(PostListViewMixin):
    model = Print
    template_name = "prints/list.html"
    permission_required = "prints.view_print"
    serializer_class = PrintSerializer

    def get_queryset(self):
        return Print.objects.filter(product__id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(id=self.kwargs.get("pk"))
        context["title"] = "Impresiones necesarias"
        context["create_url"] = reverse_lazy(
            "prints:create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        return context


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


class PrintModelRelationListView(PostListViewMixin):
    model = PrintModelRelation
    template_name = "models/list.html"
    permission_required = "prints.view_printmodelrelation"
    serializer_class = PrintModelRelationSerializer

    def get_queryset(self):
        return PrintModelRelation.objects.filter(print__id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["print"] = Print.objects.get(id=self.kwargs.get("pk"))
        context["title"] = "Modelos de la impresión"
        context["create_url"] = reverse_lazy(
            "prints:models_create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "products"
        return context


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
