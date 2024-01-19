from rest_framework import serializers

from apps.ciudata.models import Vehicle, AssignedVehicle
from apps.accounts.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'is_active',
        )


class VehicleSerializer(serializers.ModelSerializer):
    conductor = serializers.SerializerMethodField(required=False)

    def get_conductor(self, obj):
        if obj.conductor.exists():
            assigneds = obj.conductor.all().first()
            print("Conductor:  ", assigneds)
            return UsersSerializer(assigneds.user).data
        else:
            return None

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'slug',
            'plate',
            'brand',
            'model',
            'detail',
            'photo',
            'metadata',
            'conductor',
            'db_status',
        ]


class AssignedVehicleSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = AssignedVehicle
        fields = ('vehicle',)


class AssignedVehicleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignedVehicle
        fields = [
            'id',
            'user',
            'vehicle',
            'detail',
            'assigned_date',
            'metadata',
        ]

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            user = data['user']
            vehicle = data['vehicle']

            # Valida que el vehículo no esté asignado a otro usuario
            if AssignedVehicle.objects.filter(vehicle=vehicle).exists():
                raise serializers.ValidationError(
                    {'vehicle': 'El vehículo ya está asignado a otro usuario.'}
                )

            # Valida que el usuario no tenga asignado el vehículo
            if AssignedVehicle.objects.filter(user=user, vehicle=vehicle).exists():
                raise serializers.ValidationError(
                    {'user': 'El usuario ya tiene asignado un vehículo.'}
                )

        return data


class AssignedVehicleResponseSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    vehicle_detail = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        if obj.user.first_name:
            if obj.user.last_name:
                return f"{obj.user.first_name} {obj.user.last_name}"
            else:
                return f"{obj.user.first_name}"
        else:
            return obj.user.username

    def get_vehicle_detail(self, obj):
        return f"{obj.vehicle.plate} ({obj.vehicle.brand})"

    class Meta:
        model = AssignedVehicle
        fields = [
            'id',
            'user',
            'vehicle',
            'detail',
            'assigned_date',
            'metadata',
            'user_name',
            'vehicle_detail',
        ]
