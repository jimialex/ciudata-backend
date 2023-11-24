from rest_framework import serializers

from apps.ciudata.models import Area, Route, AssignedRoute


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all_'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all_'


class AssignedRoute(serializers.ModelSerializer):
    class Meta:
        model = AssignedRoute
        fields = '__all_'