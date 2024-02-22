from rest_framework import serializers

from prints.models import PrintMaterial, Print


class PrintMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintMaterial
        fields = "__all__"
        read_only_fields = ["id"]


class PrintSerializer(serializers.ModelSerializer):
    material = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = Print
        fields = "__all__"
        read_only_fields = ["id"]
