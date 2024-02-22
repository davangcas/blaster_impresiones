from rest_framework import serializers

from prints.models import Print, PrintMaterial, PrintModelRelation


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


class PrintModelRelationSerializer(serializers.ModelSerializer):
    print_model = serializers.StringRelatedField()
    print = serializers.StringRelatedField()
    x_scale = serializers.SerializerMethodField()
    y_scale = serializers.SerializerMethodField()
    z_scale = serializers.SerializerMethodField()
    print_model_id = serializers.SerializerMethodField()


    class Meta:
        model = PrintModelRelation
        fields = "__all__"
        read_only_fields = ["id"]

    def get_x_scale(self, obj):
        return obj.print_model.x_scale

    def get_y_scale(self, obj):
        return obj.print_model.y_scale

    def get_z_scale(self, obj):
        return obj.print_model.z_scale

    def get_print_model_id(self, obj):
        return obj.print_model.id
