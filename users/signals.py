from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Role


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    instance.user_permissions.clear()
    instance.user_permissions.add(*instance.role.permissions.all())


@receiver(post_save, sender=Role)
def role_post_save(sender, instance, created, **kwargs):
    for user in instance.users.all():
        user.user_permissions.clear()
        user.user_permissions.add(*instance.permissions.all())
