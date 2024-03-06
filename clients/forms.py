from clients.models import Client
from core.forms import DefaultModelForm


class ClientCreateEditForm(DefaultModelForm):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "phone_number", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].required = True
        self.fields["email"].widget.attrs["placeholder"] = "(opcional)"
