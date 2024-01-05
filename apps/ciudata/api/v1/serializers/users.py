# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models import User
from apps.ciudata.api.v1.serializers.vehicle import *
from apps.ciudata.api.v1.serializers.assignations import *
from apps.accounts.api.v1.serializers.user_profile import GroupSerializer


class UsersResponseSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url', required=False)
    # serializers.ListField(child=serializers.CharField(max_length=255))
    groups = serializers.SerializerMethodField(required=False)
    assigned_vehicle = serializers.SerializerMethodField(required=False)
    assigned_route = serializers.SerializerMethodField(required=False)
    groups_objects = serializers.SerializerMethodField()

    def get_groups(self, user):
        if user.groups.exists():
            return [group.name for group in user.groups.all()]
        else:
            return []

    def get_groups_objects(self, user):
        if user.groups.exists():
            print(user.groups.all())
            return GroupSerializer(user.groups.all(), many=True).data
        else:
            return None

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
            'groups_objects',
        )
        read_only_fields = fields


class UsersSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""
    photo = serializers.CharField(source='photo_url', required=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
        )
