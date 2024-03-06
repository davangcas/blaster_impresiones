from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from prints.models import Print, PrintModel
from prints.services import calculate_print_price


@receiver(pre_save, sender=Print)
def print_pre_save(sender, instance, **kwargs):
    instance.price = calculate_print_price(instance)


@receiver(post_save, sender=Print)
def print_post_save(sender, instance, **kwargs):
    instance.product.save()


@receiver(post_delete, sender=Print)
def print_post_delete(sender, instance, **kwargs):
    instance.g_code.delete(save=False)
    instance.product.save()


@receiver(post_delete, sender=PrintModel)
def print_model_post_delete(sender, instance, **kwargs):
    instance.file.delete(save=False)
