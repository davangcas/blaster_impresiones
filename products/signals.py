from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from products.models import ExtraProductCost, Product
from products.services import calculate_product_price


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    if instance.pk:
        instance.price = calculate_product_price(instance)
    else:
        instance.price = 0


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    instance.image.delete(save=False)


@receiver(post_save, sender=ExtraProductCost)
def extra_product_cost_post_save(sender, instance, **kwargs):
    instance.product.save()


@receiver(post_delete, sender=ExtraProductCost)
def extra_product_cost_post_delete(sender, instance, **kwargs):
    instance.product.save()
