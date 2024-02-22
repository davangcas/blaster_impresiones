from django.db.models.signals import post_delete
from django.dispatch import receiver

from products.models import Product


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    instance.image.delete(save=False)
