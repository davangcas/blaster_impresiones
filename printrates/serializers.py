from rest_framework import serializers
from printrates.models import MonthlyCost, PrintRate


class PrintRateSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = PrintRate
        fields = "__all__"
        read_only_fields = ["created_at", "id"]

    def get_rate(self, obj):
        return f"${obj.rate}"


class MonthlyCostSerializer(serializers.ModelSerializer):
    cost = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d/%m/%Y")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = MonthlyCost
        fields = "__all__"
        read_only_fields = ["created_at", "id", "updated_at"]

    def get_cost(self, obj):
        return f"${obj.cost}"
