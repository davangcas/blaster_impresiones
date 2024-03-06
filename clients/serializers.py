from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["id"]

    def get_email(self, obj):
        return obj.email or "No tiene correo electrónico"
