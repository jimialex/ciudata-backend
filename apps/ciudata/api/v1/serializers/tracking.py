
from rest_framework import serializers

from apps.ciudata.models import Tracking
from apps.ciudata.api.v1.serializers.assignations import *


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ['assigned_route', 'datetime',
                  'lat', 'lng',]


class TrackingResponseSerializer(serializers.ModelSerializer):
    assigned_route = AssignedRouteSimpleSerializer()

    class Meta:
        model = Tracking
        fields = ['assigned_route', 'datetime',
                  'lat', 'lng',]
