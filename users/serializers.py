from rest_framework import serializers

from users.models import Role, User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        ]


class RoleSerializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]

    def get_permissions(self, obj):
        return obj.get_permission_names()
