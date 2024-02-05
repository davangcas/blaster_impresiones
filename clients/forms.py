from clients.models import Client
from core.forms import DefaultModelForm


class ClientEditForm(DefaultModelForm):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "phone_number", "email")


class ClientCreateForm(DefaultModelForm):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "phone_number", "email")
