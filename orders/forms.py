from core.forms import DefaultModelForm
from orders.models import Order, OrderItem, PrintOrderItem


class OrderCreateEditForm(DefaultModelForm):
    class Meta:
        model = Order
        fields = ("client",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].label = "Cliente"
        self.fields["client"].widget.attrs["class"] = (
            "select2bs4 select2-hidden-accessible"
        )
        self.fields["client"].widget.attrs["style"] = "width: 100%;"


class OrderItemUpdateForm(DefaultModelForm):
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].label = "Producto"
        self.fields["product"].widget.attrs["class"] = (
            "select2bs4 select2-hidden-accessible"
        )
        self.fields["product"].widget.attrs["style"] = "width: 100%;"
        self.fields["product"].empty_label = "Seleccione un producto"
        self.fields["quantity"].label = "Cantidad"


class OrderItemCreateForm(OrderItemUpdateForm):
    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.pop("order_id")
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.order_id = self.order_id
        instance.save()
        return instance


class PrintOrderItemUpdateForm(DefaultModelForm):
    class Meta:
        model = PrintOrderItem
        fields = ("color",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"].label = "Color"
        self.fields["color"].widget.attrs["class"] = (
            "select2bs4 select2-hidden-accessible"
        )
        self.fields["color"].widget.attrs["style"] = "width: 100%;"
        self.fields["color"].empty_label = "Seleccione un color"
        self.fields[
            "color"
        ].queryset = self.instance.print.material.printmaterialcolor_set.all()
