from rest_framework import serializers

from orders.models import Order, OrderItem, PrintOrderItem


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    state = serializers.CharField(source="get_state_display")
    total = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
        return f"${obj.get_total_cost()}"
