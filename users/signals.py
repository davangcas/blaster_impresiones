from django.db.models.signals import post_save
from django.dispatch import receiver

from financials.models import Account
from users.models import Role, User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    instance.user_permissions.clear()
    instance.user_permissions.add(*instance.role.permissions.all())

    if not instance.account:
        instance.account = Account.objects.create(
            name=instance.username, account_type="asset"
        )
        instance.save()


@receiver(post_save, sender=Role)
def role_post_save(sender, instance, created, **kwargs):
    for user in instance.users.all():
        user.user_permissions.clear()
        user.user_permissions.add(*instance.permissions.all())
