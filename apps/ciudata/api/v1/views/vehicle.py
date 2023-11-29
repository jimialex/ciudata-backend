# -*- coding: utf-8 -*-

from apps.contrib.api.viewsets import (BaseViewset)
from apps.ciudata.api.v1.serializers.vehicle import VehicleSerializer
from apps.ciudata.models.vehicle import *
from apps.contrib.api.responses import DoneResponse
from apps.ciudata.api.v1 import codes
CREATED = "CREATED"


class VehiclesViewSet(BaseViewset):
    """Contains all users endpoints."""

    serializer_class = VehicleSerializer
    response_serializer_class = VehicleSerializer
    search_fields = [
        'plate', 'brand', 'model',
    ]
    filterset_fields = ['plate']
    ordering_fields = '__all__'
    queryset = Vehicle.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.VEHICLE_DELETED)
