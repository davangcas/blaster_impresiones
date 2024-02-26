from core.forms import DefaultModelForm
from orders.models import Order


class OrderCreateEditForm(DefaultModelForm):
    class Meta:
        model = Order
        fields = ["client", "state"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["state"].label = "Estado"
        self.fields["state"].widget.attrs["class"] = "select2bs4 select2-hidden-accessible"
        self.fields["state"].widget.attrs["style"] = "width: 100%;"
        self.fields["client"].label = "Cliente"
        self.fields["client"].widget.attrs["class"] = "select2bs4 select2-hidden-accessible"
        self.fields["client"].widget.attrs["style"] = "width: 100%;"
