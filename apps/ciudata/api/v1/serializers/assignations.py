from rest_framework import serializers
from apps.ciudata.models import Area, Route, AssignedRoute
from apps.ciudata.api.v1.serializers.route import RouteSerializer, UsersSimpleSerializer


class AssignedRouteSerializer(serializers.ModelSerializer):
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


class AssignedRouteCompleteSerializer(serializers.ModelSerializer):
    user = UsersSimpleSerializer()
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
            'user',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
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
