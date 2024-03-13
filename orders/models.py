from django.db import models

from clients.models import Client
from orders.choices import ORDER_STATE_CHOICES, ORDER_STATE_STYLES_DICT
from prints.models import Print, PrintMaterialColor
from products.models import Product


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    state = models.CharField(
        max_length=50, default="pending", blank=True, choices=ORDER_STATE_CHOICES
    )

    def __str__(self):
        return f"Orden {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_state_display(self):
        return dict(ORDER_STATE_CHOICES).get(self.state)

    def get_state_style(self):
        return ORDER_STATE_STYLES_DICT.get(self.state)

    def get_state_display_with_style(self):
        state = self.get_state_display()
        state_style = ORDER_STATE_STYLES_DICT.get(self.state)
        return f"<span class='badge badge-{state_style}'>{state}</span>"

    def get_next_state(self):
        if self.state == "pending":
            return "in_progress"
        if self.state == "in_progress":
            return "completed"
        if self.state == "completed":
            return "delivered"
        if self.state == "delivered":
            return "paid"
        return self.state

    def get_previous_state(self):
        if self.state == "in_progress":
            return "pending"
        if self.state == "completed":
            return "in_progress"
        if self.state == "delivered":
            return "completed"
        if self.state == "paid":
            return "delivered"
        return self.state


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    state = models.CharField(
        max_length=50, default="pending", blank=True, choices=ORDER_STATE_CHOICES
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_state_display(self):
        return dict(ORDER_STATE_CHOICES).get(self.state)

    def get_state_style(self):
        return ORDER_STATE_STYLES_DICT.get(self.state)

    def get_state_display_with_style(self):
        state = self.get_state_display()
        state_style = ORDER_STATE_STYLES_DICT.get(self.state)
        return f"<span class='badge badge-{state_style}'>{state}</span>"


class PrintOrderItem(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="print_order_items"
    )
    print = models.ForeignKey(
        Print, on_delete=models.CASCADE, related_name="print_order_items"
    )
    state = models.CharField(
        max_length=50, default="pending", blank=True, choices=ORDER_STATE_CHOICES
    )
    color = models.ForeignKey(
        PrintMaterialColor,
        on_delete=models.SET_NULL,
        related_name="print_order_items",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    def get_state_display(self):
        return dict(ORDER_STATE_CHOICES).get(self.state)

    def get_state_style(self):
        return ORDER_STATE_STYLES_DICT.get(self.state)

    def get_state_display_with_style(self):
        state = self.get_state_display()
        state_style = ORDER_STATE_STYLES_DICT.get(self.state)
        return f"<span class='badge badge-{state_style}'>{state}</span>"

    def get_next_state(self):
        if self.state == "pending":
            return "in_progress"
        if self.state == "in_progress":
            return "completed"
        return self.state

    def get_previous_state(self):
        if self.state == "in_progress":
            return "pending"
        if self.state == "completed":
            return "completed"
        return self.state
