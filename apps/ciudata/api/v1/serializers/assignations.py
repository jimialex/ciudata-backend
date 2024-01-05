# Django & DRF
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

# Serializers
from apps.ciudata.api.v1.serializers.route import RouteSerializer, UsersSimpleSerializer

# Models
from apps.accounts.models import User
from apps.ciudata.models import (Area, Tracking, AssignedRoute,
                                 Route, ASSIGNED, COMPLETED)


class AssignedRouteCreateSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        route = data['route']
        if route.route_assigned.exists():
            # verificamos su la ruta asignada tiene alguna asignacion sin completar
            if (route.route_assigned.filter(status=ASSIGNED).exists()):
                raise serializers.ValidationError({'route': [_('Route is already assigned.')]})
        return data

    class Meta:
        model = AssignedRoute
        fields = [
            'slug',
            'user',
            'route',
            'assigned_detail',
            'assigned_date',
            'status',
            'completed_detail',
            'completed_date',
            'geo_route',
            'metadata',
        ]


class AssignedRouteSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AssignedRoute
        fields = [
            'slug',
            'user',
            'route',
            'assigned_detail',
            'assigned_date',
            'status',
            'completed_detail',
            'completed_date',
            'geo_route',
            'metadata',
        ]


class AssignedRouteResponseSerializer(serializers.ModelSerializer):
    # user = UsersSimpleSerializer()
    route = RouteSerializer()

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'assigned_detail',
            'assigned_date',
            'status',
            'geo_route',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
        ]


class TrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracking
        fields = ['lat', 'lng', 'datetime']


class AssignedRouteCompleteSerializer(serializers.ModelSerializer):
    user = UsersSimpleSerializer()
    route = RouteSerializer()
    traking_assigned_route = serializers.SerializerMethodField()

    def get_traking_assigned_route(self, obj):
        """Return all points in traking for Assigned route"""
        if obj.traking_assigned_route is not None:
            points = obj.traking_assigned_route.all()
            return TrackingSerializer(points, many=True).data
        return {}

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'assigned_detail',
            'assigned_date',
            'status',
            'geo_route',
            'user',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
            'traking_assigned_route',
        ]


class AssignedRouteSimpleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = UsersSimpleSerializer()
    route = serializers.SerializerMethodField()

    def get_route(self, obj):
        return obj.route.name

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'route',
            'user',
            'assigned_date',
            'status',
        ]
