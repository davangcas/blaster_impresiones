from rest_framework import serializers

from financials.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["account"]
