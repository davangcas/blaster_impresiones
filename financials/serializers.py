from rest_framework import serializers

from financials.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def get_from_account(self, obj):
        from_account = "Fuentes Externas"

        if obj.from_account:
            from_account = obj.from_account.name

        return from_account

    def get_to_account(self, obj):
        to_account = "Fuentes Externas"

        if obj.to_account:
            to_account = obj.to_account.name

        return to_account

    def get_amount(self, obj):
        return f"${obj.amount}"
