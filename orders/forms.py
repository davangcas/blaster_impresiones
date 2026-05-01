from django import forms

from core.forms import DefaultForm, DefaultModelForm
from orders.choices import PRINT_ORDER_ITEM_SELECTABLE_STATE_CHOICES
from orders.models import Order, OrderItem, PrintOrderItem
from prints.models import PrintMaterialColor


class PrintOrderItemChangeStateForm(DefaultForm):
    include_footer_buttons = False

    state = forms.ChoiceField(
        label="Estado",
        choices=PRINT_ORDER_ITEM_SELECTABLE_STATE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False


class PrintOrderItemChangeColorForm(DefaultForm):
    include_footer_buttons = False

    color = forms.ModelChoiceField(
        queryset=PrintMaterialColor.objects.all().order_by("material", "color"),
        label="Color",
        widget=forms.Select(
            attrs={"class": "form-control select2bs4", "style": "width: 100%;"}
        ),
        empty_label="Seleccione un color",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False


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
