from rest_framework import serializers

from orders.models import Order, OrderItem, PrintOrderItem
from prints.serializers import PrintSerializer


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    state = serializers.CharField(source="get_state_display_with_style")
    total = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d/%m/%Y")
    state_code = serializers.CharField(source="state")

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
        return f"${obj.get_total_cost()}"


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    total = serializers.SerializerMethodField()
    state = serializers.CharField(source="get_state_display_with_style")
    state_code = serializers.CharField(source="state")

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_total(self, obj):
        return f"${obj.get_cost()}"


class PrintOrderItemSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer()
    print = PrintSerializer()
    state = serializers.CharField(source="get_state_display_with_style")
    state_code = serializers.CharField(source="state")
    color = serializers.SerializerMethodField()

    class Meta:
        model = PrintOrderItem
        fields = "__all__"

    def get_color(self, obj):
        return obj.color.color if obj.color else "-"
