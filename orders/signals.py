from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from orders.models import OrderItem, PrintOrderItem, Order


@receiver(post_save, sender=Order)
def update_order(sender, instance, **kwargs):
    if instance.state in ("delivered", "paid"):
        for item in instance.items.all():
            item.state = instance.state
            item.save()


@receiver(pre_save, sender=OrderItem)
def update_order_item(sender, instance, **kwargs):
    instance.price = instance.product.price


@receiver(post_save, sender=OrderItem)
def generate_print_order_item(sender, instance, **kwargs):
    instance_prints = instance.product.print_set.all()

    for print in instance_prints:
        current_print_order_items = PrintOrderItem.objects.filter(
            order_item=instance, print=print
        ).count()
        required_print_order_items = instance.quantity
        print_order_items_to_create = (
            required_print_order_items - current_print_order_items
        )

        if print_order_items_to_create > 0:
            for iteration in range(print_order_items_to_create):
                PrintOrderItem.objects.create(
                    order_item=instance, print=print, state="pending"
                )
        elif print_order_items_to_create < 0:
            print_order_items_to_delete = abs(print_order_items_to_create)
            for iteration in range(print_order_items_to_delete):
                PrintOrderItem.objects.filter(
                    order_item=instance, print=print, state="pending"
                ).first().delete()

    if instance.state == "completed":
        all_order_items_completed = instance.order.items.filter(
            state="completed"
        ).count()
        all_order_items = instance.order.items.count()

        if all_order_items_completed == all_order_items:
            instance.order.state = "completed"
            instance.order.save()

        instance.product.stock += instance.quantity
        instance.product.save()

    elif instance.state == "pending":
        instance.order.state = "pending"
        instance.order.save()

    elif instance.state == "in_progress":
        instance.order.state = "in_progress"
        instance.order.save()

    elif instance.state == "delivered":
        instance.product.stock -= instance.quantity
        instance.product.save()


@receiver(post_save, sender=PrintOrderItem)
def update_print_order_item(sender, instance, **kwargs):
    if instance.state == "completed":
        all_order_items_completed = instance.order_item.print_order_items.filter(
            state="completed"
        ).count()
        all_order_items = instance.order_item.print_order_items.count()

        if all_order_items_completed == all_order_items:
            instance.order_item.state = "completed"
            instance.order_item.save()

    elif instance.state == "in_progress":
        instance.order_item.state = "in_progress"
        instance.order_item.save()
        instance.color.remaining -= instance.print.grams
        instance.color.save()

    elif instance.state == "pending":
        instance.order_item.state = "pending"
        instance.order_item.save()
