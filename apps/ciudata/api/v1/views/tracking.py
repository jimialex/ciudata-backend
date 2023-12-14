# -*- coding: utf-8 -*-

from apps.contrib.api.viewsets import (BaseViewset, )
from apps.ciudata.api.v1.serializers.tracking import *
from apps.ciudata.models.tracking import *
from apps.contrib.api.responses import DoneResponse
from apps.ciudata.api.v1 import codes
CREATED = "CREATED"


class TrackingsViewSet(BaseViewset):
    """Contains all Tracking endpoints."""
    serializer_class = TrackingSerializer
    response_serializer_class = TrackingResponseSerializer
    search_fields = ['datetime', 'assigned_route']
    filterset_fields = ['datetime']
    ordering_fields = '__all__'
    queryset = Tracking.objects.all()
    pagination_class = None
