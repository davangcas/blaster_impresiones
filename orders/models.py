from django.db import models

from clients.models import Client
from prints.models import Print, PrintMaterialColor
from products.models import Product


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    state = models.CharField(max_length=50, default="pending", blank=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class PrintOrderItem(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="print_order_items"
    )
    print = models.ForeignKey(
        Print, on_delete=models.CASCADE, related_name="print_order_items"
    )
    state = models.CharField(max_length=50, default="pending", blank=True)
    color = models.ForeignKey(
        PrintMaterialColor, on_delete=models.CASCADE, related_name="print_order_items"
    )

    def __str__(self):
        return str(self.id)
