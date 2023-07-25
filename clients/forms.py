from django import forms

from clients.models import Client


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "phone_number", "email")


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("first_name", "last_name", "phone_number", "email")
