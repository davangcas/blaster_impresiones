from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id"]

    def get_price(self, obj):
        return f"${obj.price}"
