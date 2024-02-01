# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.db.models import Sum
from apps.accounts.models import User
from apps.ciudata.models import (ASSIGNED, COMPLETED)
from apps.ciudata.api.v1.serializers.vehicle import *
from apps.ciudata.api.v1.serializers.assignations import *
from apps.accounts.api.v1.serializers.user_profile import GroupSerializer
from rest_framework.serializers import raise_errors_on_nested_writes
from django.contrib.auth.models import Group


class UsersResponseSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url', required=False)
    photo_simple = serializers.SerializerMethodField()
    # serializers.ListField(child=serializers.CharField(max_length=255))
    groups = serializers.SerializerMethodField(required=False)
    assigned_vehicle = serializers.SerializerMethodField(required=False)
    assigned_route = serializers.SerializerMethodField(required=False)
    completed_route = serializers.SerializerMethodField(required=False)
    distance_assigned = serializers.SerializerMethodField(required=False)
    groups_objects = serializers.SerializerMethodField()

    def get_photo_simple(self, user):
        return str(user.photo) if user.photo else None

    def get_groups(self, user):
        group_names = user.groups.values_list('name', flat=True)  # Obtiene solo los nombres en una consulta
        return list(group_names)  # Convierte el QuerySet a lista

    def get_groups_objects(self, user):
        if user.groups.exists():
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
            assigneds = user.assigned_route.filter(status=ASSIGNED)
            return AssignedRouteResponseSerializer(assigneds, many=True).data
        else:
            return []

    def get_completed_route(self, user):
        if user.assigned_route.exists():
            assigneds = user.assigned_route.filter(status=COMPLETED)
            return AssignedRouteResponseSerializer(assigneds, many=True).data
        else:
            return []

    def get_distance_assigned(self, user):
        # Retorna la suma de todas las distancias de ruta asignadas em [m]
        distance = 0
        if user.assigned_route.exists():
            for item in user.assigned_route.all():
                distance += item.route.metadata.get('distance', 0)
        return distance

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'photo_simple',
            'photo',
            'lang',
            'is_active',
            'distance_assigned',
            'groups',
            'assigned_vehicle',
            'assigned_route',
            'completed_route',
            'groups_objects',
        )
        read_only_fields = fields


class UsersSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""
    photo = serializers.ImageField(required=False)
    photo_simple = serializers.SerializerMethodField(required=False, read_only=True)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    is_active = serializers.CharField(read_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    def get_photo_simple(self, user):
        return str(user.photo) if user.photo else None

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'photo_simple',
            'lang',
            'is_active',
            'groups',
        )
