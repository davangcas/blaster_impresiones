from django.db import models

from financials.choices import ACCOUNT_TYPES


class Account(models.Model):
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    @classmethod
    def calculate_equity(cls):
        assets = (
            cls.objects.filter(account_type="asset").aggregate(
                total=models.Sum("balance")
            )["total"]
            or 0
        )
        liabilities = (
            cls.objects.filter(account_type="liability").aggregate(
                total=models.Sum("balance")
            )["total"]
            or 0
        )
        return assets - liabilities


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )

    def __str__(self):
        return self.description


class Sale(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    related_transaction = models.ManyToManyField(Transaction, related_name="sales")

    def __str__(self):
        return f"{self.date} - {self.amount}"
