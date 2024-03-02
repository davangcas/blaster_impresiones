from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    RedirectView,
    UpdateView,
)
import ast

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from orders.forms import (
    OrderCreateEditForm,
    OrderItemCreateForm,
    OrderItemUpdateForm,
    PrintOrderItemUpdateForm,
)
from orders.models import Order, OrderItem, PrintOrderItem
from orders.serializers import (
    OrderItemSerializer,
    OrderSerializer,
    PrintOrderItemSerializer,
)
from prints.serializers import PrintModelRelationSerializer


class OrderListView(PostListViewMixin):
    model = Order
    template_name = "orders/list.html"
    permission_required = "orders.view_order"
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().select_related("client").order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pedidos"
        context["create_url"] = reverse_lazy("orders:create")
        context["active_section"] = "orders"
        return context


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


class OrderItemListView(PostListViewMixin):
    model = OrderItem
    template_name = "items/list.html"
    permission_required = "orders.view_orderitem"
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs.get("pk")).select_related(
            "product"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Items"
        context["create_url"] = reverse_lazy(
            "orders:items_create", kwargs={"pk": self.kwargs.get("pk")}
        )
        context["active_section"] = "orders"
        context["order"] = Order.objects.get(id=self.kwargs.get("pk"))
        return context


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


class PrintOrderItemListView(PostListViewMixin):
    model = PrintOrderItem
    template_name = "print_order_items/list.html"
    permission_required = "orders.view_printorderitem"
    serializer_class = PrintOrderItemSerializer

    def get_queryset(self):
        return PrintOrderItem.objects.filter(
            order_item_id=self.kwargs.get("pk")
        ).select_related("print")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Impresiones"
        context["active_section"] = "orders"
        context["order_item"] = OrderItem.objects.get(id=self.kwargs.get("pk"))
        return context


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
    serializer_class = PrintModelRelationSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalles de la impresion"
        context["active_section"] = "orders"
        context["order_item_id"] = self.get_object().order_item_id
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_object().print.printmodelrelation_set.all()
        data = self.serializer_class(self.object_list, many=True).data
        response = JsonResponse({"data": data}, safe=False)
        return response
