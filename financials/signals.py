from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from financials.models import Transaction


@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, created, **kwargs):
    if instance.from_account:
        instance.from_account.balance -= instance.amount
        instance.from_account.save()

    if instance.to_account:
        instance.to_account.balance += instance.amount
        instance.to_account.save()


@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    if instance.from_account:
        instance.from_account.balance += instance.amount
        instance.from_account.save()

    if instance.to_account:
        instance.to_account.balance -= instance.amount
        instance.to_account.save()
