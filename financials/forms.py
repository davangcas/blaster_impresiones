from django import forms

from core.fields import CustomPriceDecimalField
from core.forms import DefaultModelForm
from financials.models import Transaction


class TransactionCreateEditForm(DefaultModelForm):
    amount = CustomPriceDecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Monto",
        required=True,
        max_digits=15,
        decimal_places=2,
        initial=0,
    )

    class Meta:
        model = Transaction
        fields = ("from_account", "to_account", "amount", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["from_account"].label = "Cuenta Origen"
        self.fields["from_account"].widget.attrs[
            "class"
        ] = "select2bs4 select2-hidden-accessible"
        self.fields["from_account"].widget.attrs["style"] = "width: 100%;"
        self.fields["from_account"].empty_label = "Cuenta Externa"
        self.fields["to_account"].label = "Cuenta Destino"
        self.fields["to_account"].widget.attrs[
            "class"
        ] = "select2bs4 select2-hidden-accessible"
        self.fields["to_account"].widget.attrs["style"] = "width: 100%;"
        self.fields["to_account"].empty_label = "Cuenta Externa"
        self.fields["description"].label = "Descripción"
        self.fields["description"].required = True

    def clean_to_account(self):
        if self.cleaned_data["from_account"] == self.cleaned_data["to_account"]:
            raise forms.ValidationError(
                "La cuenta origen y la cuenta destino no pueden ser iguales"
            )
        return self.cleaned_data["to_account"]


class TransactionCreateFromAccountForm(TransactionCreateEditForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get("from_account")
        to_account = cleaned_data.get("to_account")
        proceed_with_validation = False

        if from_account and from_account.user == self.user:
            proceed_with_validation = True

        if to_account and to_account.user == self.user:
            proceed_with_validation = True

        if not proceed_with_validation:
            raise forms.ValidationError(
                "No puedes realizar transacciones entre cuentas de otros usuarios"
            )

        return cleaned_data
