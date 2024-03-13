from django.db import models
from simple_history.models import HistoricalRecords

from financials.choices import ACCOUNT_TYPES
from users.models import User


class Account(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="accounts", blank=True, null=True
    )
    historical = HistoricalRecords()

    def __str__(self):
        return self.name or self.user.username

    @property
    def incomes(self):
        return (
            self.incoming_transactions.aggregate(models.Sum("amount"))["amount__sum"]
            or 0
        )

    @property
    def expenses(self):
        return (
            self.outgoing_transactions.aggregate(models.Sum("amount"))["amount__sum"]
            or 0
        )


class Transaction(models.Model):
    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="outgoing_transactions",
        null=True,
        blank=True,
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="incoming_transactions",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    historical = HistoricalRecords()

    def __str__(self):
        return self.description

    def get_from_account_name(self):
        return self.from_account.name if self.from_account else "Fuentes Externas"

    def get_to_account_name(self):
        return self.to_account.name if self.to_account else "Fuentes Externas"
