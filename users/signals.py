from django.db import transaction
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from printrates.services import generate_print_rate
from users.models import Role, User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    current_permissions = list(instance.user_permissions.all())
    new_permissions = list(instance.role.permissions.all())
    instance.accounts.all().update(name=instance.username)
    generate_print_rate()

    if created or set(new_permissions) != set(current_permissions):
        instance.user_permissions.clear()
        instance.user_permissions.add(*instance.role.permissions.all())


@receiver(post_delete, sender=User)
def user_post_delete(sender, instance, **kwargs):
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
