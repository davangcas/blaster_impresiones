from rest_framework import serializers

from printrates.models import MonthlyCost, PrintRate, PrintRateVariables


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


class PrintRateVariablesSerializer(serializers.ModelSerializer):
    failure_percentage = serializers.SerializerMethodField()
    maintenance_cost = serializers.SerializerMethodField()
    minutes_spent_per_print = serializers.SerializerMethodField()
    extra_percentage = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d/%m/%Y")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = PrintRateVariables
        fields = "__all__"
        read_only_fields = ["created_at", "id", "updated_at"]

    def get_failure_percentage(self, obj):
        return f"{obj.failure_percentage}%"

    def get_maintenance_cost(self, obj):
        return f"${obj.maintenance_cost}"

    def get_minutes_spent_per_print(self, obj):
        return f"{obj.minutes_spent_per_print} minutos"

    def get_extra_percentage(self, obj):
        return f"{obj.extra_percentage}%"
