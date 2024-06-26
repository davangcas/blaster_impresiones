import ast

from django.contrib import messages
from django.db.models import CharField, F, Sum, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from core.mixins import CustomAdminViewMixin, CustomDatatablesJsonMixin
from orders.forms import (
    OrderCreateEditForm,
    OrderItemCreateForm,
    OrderItemUpdateForm,
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
        if column == "created":
            return timezone.localtime(row.created).strftime("%d/%m/%Y %H:%M")
        if column == "state":
            return row.get_state_display_with_style()
        if column == "total":
            return f"${row.total}"
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
        return context


class PrintOrderItemDatatableView(CustomDatatablesJsonMixin):
    permission_required = "orders.view_printorderitem"
    model = PrintOrderItem
    columns = [
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
            super().get_initial_queryset().filter(order_item_id=self.kwargs.get("pk"))
        )

    def render_column(self, row, column):
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


class PrintOrderItemChangeStateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        instance = PrintOrderItem.objects.get(id=kwargs.get("pk"))
        next_step = ast.literal_eval(self.request.GET.get("next_step", "True"))
        state = instance.get_next_state()
        return_url = reverse_lazy(
            "orders:print_order_items", kwargs={"pk": instance.order_item_id}
        )

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
