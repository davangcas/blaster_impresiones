from django.db.models.signals import post_delete
from django.dispatch import receiver

from prints.models import Print, PrintModel


@receiver(post_delete, sender=Print)
def print_post_delete(sender, instance, **kwargs):
    instance.g_code.delete(save=False)


@receiver(post_delete, sender=PrintModel)
def print_model_post_delete(sender, instance, **kwargs):
    instance.file.delete(save=False)
