from rest_framework import serializers

from apps.ciudata.models import Vehicle, AssignedVehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'slug',
            'plate',
            'brand',
            'model',
            'detail',
            'photo',
            'metadata',
            'db_status',
        ]


class AssignedVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedVehicle
        fields = '__all_'
