# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models import User
from apps.ciudata.api.v1.serializers.vehicle import *
from apps.ciudata.api.v1.serializers.assignations import *


class UsersSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url')
    groups = serializers.SerializerMethodField()  # serializers.ListField(child=serializers.CharField(max_length=255))
    assigned_vehicle = serializers.SerializerMethodField()
    assigned_route = serializers.SerializerMethodField()

    def get_groups(self, user):
        if user.groups.exists():
            return [group.name for group in user.groups.all()]
        else:
            return []

    def get_assigned_vehicle(self, user):
        if user.assigned_vehicle.exists():
            assigneds = user.assigned_vehicle.all()
            return AssignedVehicleSerializer(assigneds, many=True).data
        else:
            return []

    def get_assigned_route(self, user):
        if user.assigned_route.exists():
            assigneds = user.assigned_route.all()
            return AssignedRouteResponseSerializer(assigneds, many=True).data
        else:
            return []

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'lang',
            'is_active',
            'groups',
            'assigned_vehicle',
            'assigned_route',
        )
        read_only_fields = fields
