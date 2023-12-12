
from rest_framework import serializers

from apps.ciudata.models import Tracking


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ['assigned_route', 'datetime',
                  'lat', 'lng',]
