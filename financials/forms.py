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
        self.fields["from_account"].queryset = self.fields[
            "from_account"
        ].queryset.filter(user__isnull=False, account_type="USER") | self.fields[
            "from_account"
        ].queryset.filter(
            user__isnull=True, account_type="ORGANIZATION"
        )
        self.fields["to_account"].label = "Cuenta Destino"
        self.fields["to_account"].widget.attrs[
            "class"
        ] = "select2bs4 select2-hidden-accessible"
        self.fields["to_account"].widget.attrs["style"] = "width: 100%;"
        self.fields["to_account"].empty_label = "Cuenta Externa"
        self.fields["to_account"].queryset = self.fields["to_account"].queryset.filter(
            user__isnull=False, account_type="USER"
        ) | self.fields["to_account"].queryset.filter(
            user__isnull=True, account_type="ORGANIZATION"
        )
        self.fields["description"].label = "Concepto"
        self.fields["description"].required = True

    def clean_to_account(self):
        from_account = self.cleaned_data.get("from_account")
        to_account = self.cleaned_data.get("to_account")

        if from_account == to_account:
            raise forms.ValidationError(
                "La cuenta origen y la cuenta destino no pueden ser iguales"
            )

        return self.cleaned_data["to_account"]


class TransactionCreateFromAccountForm(TransactionCreateEditForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_from_account(self):
        from_account = self.cleaned_data["from_account"]

        if not from_account or from_account.user != self.user:
            raise forms.ValidationError(
                "No puedes realizar transacciones desde cuentas que no te pertenecen"
            )

        return from_account
