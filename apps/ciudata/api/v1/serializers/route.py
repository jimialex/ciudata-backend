from rest_framework import serializers

from apps.ciudata.models import Area, Route, AssignedRoute


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['slug', 'name', 'geofence']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'slug',
            'name',
            'area',
            'geo_route',
        ]


class AssignedRoute(serializers.ModelSerializer):
    class Meta:
        model = AssignedRoute
        fields = '__all_'
