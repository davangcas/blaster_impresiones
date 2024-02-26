from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.mixins import CustomAdminViewMixin, PostListViewMixin
from orders.forms import OrderCreateEditForm
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderListView(PostListViewMixin):
    model = Order
    template_name = "orders/list.html"
    permission_required = "orders.view_order"
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().select_related("client").order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ordenes"
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
