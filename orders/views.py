import ast

from django.contrib import messages
from django.db import transaction
from django.db.models import CharField, F, Sum, Value
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from core.mixins import (
    CustomAdminViewMixin,
    CustomDatatablesJsonMixin,
    DeleteMultipleObjectsMixin,
)
from core.services import get_select_checkbox
from orders.choices import ORDER_ITEM_PRINT_EDIT_STATES
from orders.forms import (
    OrderCreateEditForm,
    OrderItemCreateForm,
    OrderItemUpdateForm,
    PrintOrderItemChangeColorForm,
    PrintOrderItemChangeStateForm,
    PrintOrderItemUpdateForm,
)
from orders.models import Order, OrderItem, PrintOrderItem
from orders.services import (
    get_order_buttons,
    get_order_item_buttons,
    get_print_order_item_buttons,
)
from prints.models import PrintModelRelation


class OrderListView(CustomAdminViewMixin, TemplateView):
    model = Order
    template_name = "orders/list.html"
    permission_required = "orders.view_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pedidos"
        context["create_url"] = reverse_lazy("orders:create")
        context["active_section"] = "orders"
        context["json_view_url"] = reverse_lazy("orders:json")
        return context


class OrderDatatableView(CustomDatatablesJsonMixin):
    permission_required = "orders.view_order"
    model = Order
    columns = ["id", "created", "client_full_name", "state", "total", "actions"]

    def get_initial_queryset(self):
        queryset = super().get_initial_queryset()
        queryset = queryset.annotate(
            total=Sum(F("items__price") * F("items__quantity")),
            client_full_name=Concat(
                F("client__first_name"),
                Value(" "),
                F("client__last_name"),
                output_field=CharField(),
            ),
        )
        return queryset

    def render_column(self, row, column):
        if column == "id":
            return get_select_checkbox(row)
        if column == "created":
            return timezone.localtime(row.created).strftime("%d/%m/%Y %H:%M")
        if column == "state":
            return row.get_state_display_with_style()
        if column == "total":
            total = row.total or 0
            return f"${total}"
        if column == "actions":
            return get_order_buttons(row)
        return super().render_column(row, column)


class OrderCreateView(CustomAdminViewMixin, CreateView):
    model = Order
    template_name = "orders/create.html"
    success_url = reverse_lazy("orders:list")
    form_class = OrderCreateEditForm
    permission_required = "orders.add_order"

    def form_valid(self, form):
        messages.success(self.request, "Pedido creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el pedido")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear pedido"
        context["cancel_url"] = reverse_lazy("orders:list")
        context["active_section"] = "orders"
        return context


class OrderUpdateView(CustomAdminViewMixin, UpdateView):
    model = Order
    template_name = "orders/update.html"
    success_url = reverse_lazy("orders:list")
    form_class = OrderCreateEditForm
    permission_required = "orders.change_order"

    def form_valid(self, form):
        messages.success(self.request, "Pedido actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el pedido")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar pedido"
        context["cancel_url"] = reverse_lazy("orders:list")
        context["active_section"] = "orders"
        return context


class OrderDeleteView(CustomAdminViewMixin, DeleteView):
    model = Order
    template_name = "orders/delete.html"
    success_url = reverse_lazy("orders:list")
    permission_required = "orders.delete_order"

    def get_success_url(self):
        messages.success(self.request, "Pedido eliminado correctamente")
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar pedido"
        context["cancel_url"] = reverse_lazy("orders:list")
        context["active_section"] = "orders"
        return context


class OrderDeleteMultipleView(DeleteMultipleObjectsMixin):
    model = Order
    permission_required = "orders.delete_order"


class OrderItemListView(CustomAdminViewMixin, DetailView):
    model = Order
    template_name = "items/list.html"
    permission_required = "orders.view_orderitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Items"

        if self.get_object().state not in ("paid", "delivered"):
            context["create_url"] = reverse_lazy(
                "orders:items_create", kwargs={"pk": self.kwargs.get("pk")}
            )

        context["active_section"] = "orders"
        context["json_view_url"] = reverse_lazy(
            "orders:items_json", kwargs={"pk": self.kwargs.get("pk")}
        )
        return context


class OrderItemDatatableView(CustomDatatablesJsonMixin):
    permission_required = "orders.view_orderitem"
    model = OrderItem
    columns = ["product.name", "quantity", "state", "total", "actions"]

    def get_initial_queryset(self):
        queryset = super().get_initial_queryset().filter(order_id=self.kwargs.get("pk"))
        queryset = queryset.annotate(total=F("price") * F("quantity"))
        return queryset

    def render_column(self, row, column):
        if column == "state":
            return row.get_state_display_with_style()
        if column == "total":
            return f"${row.total}"
        if column == "actions":
            return get_order_item_buttons(row)
        return super().render_column(row, column)


class OrderItemCreateView(CustomAdminViewMixin, CreateView):
    model = OrderItem
    template_name = "items/create.html"
    form_class = OrderItemCreateForm
    permission_required = "orders.add_orderitem"

    def get_success_url(self):
        return reverse_lazy("orders:items", kwargs={"pk": self.kwargs.get("pk")})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["order_id"] = self.kwargs.get("pk")
        return form_kwargs

    def form_valid(self, form):
        messages.success(self.request, "Item creado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el item")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear item"
        context["cancel_url"] = reverse_lazy("orders:list")
        context["active_section"] = "orders"
        return context


class OrderItemUpdateView(CustomAdminViewMixin, UpdateView):
    model = OrderItem
    template_name = "items/update.html"
    form_class = OrderItemUpdateForm
    permission_required = "orders.change_orderitem"

    def get_success_url(self):
        return reverse_lazy("orders:items", kwargs={"pk": self.object.order_id})

    def form_valid(self, form):
        messages.success(self.request, "Item actualizado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el item")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar item"
        context["cancel_url"] = reverse_lazy(
            "orders:items", kwargs={"pk": self.object.order_id}
        )
        context["active_section"] = "orders"
        return context


class OrderItemDeleteView(CustomAdminViewMixin, DeleteView):
    model = OrderItem
    template_name = "items/delete.html"
    permission_required = "orders.delete_orderitem"

    def get_success_url(self):
        messages.success(self.request, "Item eliminado correctamente")
        return reverse_lazy("orders:items", kwargs={"pk": self.object.order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminar item"
        context["cancel_url"] = reverse_lazy(
            "orders:items", kwargs={"pk": self.object.order_id}
        )
        context["active_section"] = "orders"
        return context


class PrintOrderItemListView(CustomAdminViewMixin, DetailView):
    model = OrderItem
    template_name = "print_order_items/list.html"
    permission_required = "orders.view_printorderitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Impresiones"
        context["active_section"] = "orders"
        context["json_view_url"] = reverse_lazy(
            "orders:print_order_items_json", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["order_item_allows_print_edit"] = (
            self.object.state in ORDER_ITEM_PRINT_EDIT_STATES
        )
        return context


class PrintOrderItemDatatableView(CustomDatatablesJsonMixin):
    permission_required = "orders.view_printorderitem"
    model = PrintOrderItem
    columns = [
        "id",
        "print.hours",
        "print.minutes",
        "print.grams",
        "print.material.name",
        "color.color",
        "state",
        "actions",
    ]

    def get_initial_queryset(self):
        return (
            super()
            .get_initial_queryset()
            .filter(order_item_id=self.kwargs.get("pk"))
            .select_related("order_item")
        )

    def render_column(self, row, column):
        if column == "id":
            return get_select_checkbox(row)
        if column == "color.color":
            return row.color.color if row.color else "-"
        if column == "state":
            return row.get_state_display_with_style()
        if column == "actions":
            return get_print_order_item_buttons(row)
        return super().render_column(row, column)


class PrintOrderItemUpdateView(CustomAdminViewMixin, UpdateView):
    model = PrintOrderItem
    template_name = "print_order_items/update.html"
    form_class = PrintOrderItemUpdateForm
    permission_required = "orders.change_printorderitem"

    def dispatch(self, request, *args, **kwargs):
        try:
            obj = PrintOrderItem.objects.select_related("order_item").get(
                pk=kwargs.get("pk")
            )
        except PrintOrderItem.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)
        if obj.order_item.state not in ORDER_ITEM_PRINT_EDIT_STATES:
            messages.error(
                request,
                "No se puede editar el color: el ítem de la orden no está pendiente ni en progreso.",
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    "orders:print_order_items", kwargs={"pk": obj.order_item_id}
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        instance = self.get_object()
        instance.order_item.state = "pending"
        instance.state = "pending"
        instance.order_item.save()
        instance.save()
        return reverse_lazy(
            "orders:print_order_items", kwargs={"pk": self.object.order_item_id}
        )

    def form_valid(self, form):
        messages.success(
            self.request, "Color de la impresion actualizado correctamente"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el color de la impresion")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Actualizar color de la impresion"
        context["cancel_url"] = reverse_lazy(
            "orders:print_order_items", kwargs={"pk": self.object.order_item_id}
        )
        context["active_section"] = "orders"
        return context


class PrintOrderItemChangeStateFormView(CustomAdminViewMixin, TemplateView):
    """Devuelve el fragmento del formulario para el modal de cambiar estado (GET)."""

    template_name = "print_order_items/partials/change_state_form.html"
    permission_required = "orders.change_printorderitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PrintOrderItemChangeStateForm()
        return context


class PrintOrderItemChangeStateMultipleView(CustomAdminViewMixin, View):
    """Actualiza el estado de las impresiones seleccionadas (POST)."""

    permission_required = "orders.change_printorderitem"

    def post(self, request, *args, **kwargs):
        form = PrintOrderItemChangeStateForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Datos inválidos",
                    "errors": form.errors,
                },
                status=400,
            )
        selected_ids = request.POST.getlist("selected_ids[]")
        new_state = form.cleaned_data["state"]
        queryset = PrintOrderItem.objects.filter(pk__in=selected_ids).select_related(
            "order_item",
            "order_item__order",
            "color",
            "print",
        )
        if any(
            p.order_item.state not in ORDER_ITEM_PRINT_EDIT_STATES for p in queryset
        ):
            return JsonResponse(
                {
                    "success": False,
                    "message": "No se puede modificar: el ítem de la orden no está pendiente ni en progreso.",
                },
                status=403,
            )
        with transaction.atomic():
            updated = 0
            for print_order_item in queryset:
                print_order_item.state = new_state
                print_order_item.save(update_fields=["state"])
                updated += 1
        return JsonResponse(
            {
                "success": True,
                "message": f"Estado actualizado correctamente ({updated} impresión/es).",
            }
        )


class PrintOrderItemChangeColorFormView(CustomAdminViewMixin, TemplateView):
    """Devuelve el fragmento del formulario para el modal de especificar color (GET)."""

    template_name = "print_order_items/partials/change_color_form.html"
    permission_required = "orders.change_printorderitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PrintOrderItemChangeColorForm()
        return context


class PrintOrderItemChangeColorMultipleView(CustomAdminViewMixin, View):
    """Actualiza el color de las impresiones seleccionadas (POST). Solo aplica a items cuyo material coincide con el color elegido."""

    permission_required = "orders.change_printorderitem"

    def post(self, request, *args, **kwargs):
        form = PrintOrderItemChangeColorForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Datos inválidos",
                    "errors": form.errors,
                },
                status=400,
            )
        selected_ids = request.POST.getlist("selected_ids[]")
        color = form.cleaned_data["color"]
        # Solo actualizar items cuyo print tiene el mismo material que el color elegido
        updated = PrintOrderItem.objects.filter(
            pk__in=selected_ids,
            print__material=color.material,
            order_item__state__in=ORDER_ITEM_PRINT_EDIT_STATES,
        ).update(color=color)
        return JsonResponse(
            {
                "success": True,
                "message": f"Color aplicado correctamente a {updated} impresión/es.",
            }
        )


class PrintOrderItemChangeStateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        instance = PrintOrderItem.objects.select_related("order_item").get(
            id=kwargs.get("pk")
        )
        next_step = ast.literal_eval(self.request.GET.get("next_step", "True"))
        state = instance.get_next_state()
        return_url = reverse_lazy(
            "orders:print_order_items", kwargs={"pk": instance.order_item_id}
        )

        if instance.order_item.state not in ORDER_ITEM_PRINT_EDIT_STATES:
            messages.error(
                self.request,
                "No se puede cambiar el estado: el ítem de la orden no está pendiente ni en progreso.",
            )
            return return_url

        if not instance.color:
            messages.error(self.request, "Primero debes seleccionar un color")
            return return_url

        if not next_step:
            state = instance.get_previous_state()

        instance.state = state
        instance.save()
        messages.success(self.request, "Estado del item de impresion actualizado")
        return return_url


class OrderChangeStateRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        instance = Order.objects.get(id=kwargs.get("pk"))
        return_url = reverse_lazy("orders:list")
        instance.state = instance.get_next_state()
        instance.save()
        messages.success(self.request, "Orden modificada correctamente")
        return return_url


class PrintOrderItemDetailView(CustomAdminViewMixin, DetailView):
    model = PrintOrderItem
    template_name = "print_order_items/detail.html"
    permission_required = "orders.view_printorderitem"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Modelos de la impresion"
        context["active_section"] = "orders"
        context["json_view_url"] = reverse_lazy(
            "orders:print_order_items_models_json",
            kwargs={"pk": self.get_object().print.pk},
        )
        return context


class PrintOrderItemModelsDatatableView(CustomDatatablesJsonMixin):
    permission_required = "orders.view_printorderitem"
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
        return super().get_initial_queryset().filter(print_id=self.kwargs.get("pk"))

    def render_column(self, row, column):
        if column == "actions":
            if not row.print_model.file:
                return "-"
            return f"""
                <a href="{row.print_model.file.url}" class="btn btn-primary" target="_blank">
                    <i class="fas fa-download"></i>
                </a>
            """
        return super().render_column(row, column)
