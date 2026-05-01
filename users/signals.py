from django.db import transaction
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from financials.models import ACCOUNT_TYPES, Account
from printrates.services import generate_print_rate
from users.models import Role, User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    current_permissions = list(instance.user_permissions.all())
    new_permissions = list(instance.role.permissions.all())

    if not instance.accounts.all().exists():
        Account.objects.get_or_create(
            user=instance, name=instance.username, account_type=ACCOUNT_TYPES[1][0]
        )

    instance.accounts.all().update(name=instance.username)

    if created or set(new_permissions) != set(current_permissions):
        instance.user_permissions.clear()
        instance.user_permissions.add(*instance.role.permissions.all())


@receiver(post_save, sender=User)
def user_recalculate_print_rate(sender, instance, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields is not None and not any(
        f in update_fields for f in ("salary", "is_active")
    ):
        return
    generate_print_rate()


@receiver(post_delete, sender=User)
def user_delete_recalculate_print_rate(sender, instance, **kwargs):
    generate_print_rate()


@receiver(m2m_changed, sender=Role.permissions.through)
def role_permissions_changed(
    sender, instance, action, reverse, model, pk_set, **kwargs
):
    if action in ("post_add", "post_remove", "post_clear"):
        new_permissions = list(instance.permissions.all())

        with transaction.atomic():
            for user in instance.users.prefetch_related("user_permissions").all():
                current_permissions = list(user.user_permissions.all())

                if set(new_permissions) != set(current_permissions):
                    user.user_permissions.clear()
                    user.user_permissions.add(*new_permissions)
                    user.save()
