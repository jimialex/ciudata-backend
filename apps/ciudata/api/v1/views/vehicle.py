# -*- coding: utf-8 -*-
from apps.contrib.api.responses import Response

# The class VehiclesViewSet is a combination of BaseViewset and PermissionViewSet.
from apps.contrib.api.viewsets import (BaseViewset,
                                       PermissionViewSet,
                                       MixinPagination)
from apps.ciudata.api.v1.serializers.vehicle import (VehicleSerializer, AssignedVehicleCreateSerializer,
                                                     AssignedVehicleResponseSerializer)
from apps.ciudata.models.vehicle import *
from apps.contrib.api.responses import DoneResponse
from apps.ciudata.api.v1 import codes
from rest_framework.permissions import IsAuthenticated

CREATED = "CREATED"


class VehiclesViewSet(BaseViewset, PermissionViewSet):
    """Contains all users endpoints."""

    # pagination_class = None
    permission_classes = [IsAuthenticated,]
    serializer_class = VehicleSerializer
    response_serializer_class = VehicleSerializer
    search_fields = [
        'plate', 'brand', 'model',
    ]
    filterset_fields = ['plate', ]
    ordering_fields = '__all__'
    queryset = Vehicle.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.VEHICLE_DELETED)

    def perform_destroy(self, instance):
        if instance.conductor.exists():
            assigned = instance.conductor.first()
            assignement = AssignedVehicle.objects.get(pk=assigned.id)
            assignement.delete()
        instance.delete()

    def unassigned(self, request):
        queryset = self.get_queryset().filter(conductor__isnull=True).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AssignedVehiclesViewSet(BaseViewset, PermissionViewSet):
    """Contains all users endpoints."""

    # pagination_class = None
    permission_classes = [IsAuthenticated,]
    serializer_class = AssignedVehicleCreateSerializer
    response_serializer_class = AssignedVehicleResponseSerializer
    search_fields = [
        'user', 'vehicle', 'detail', 'assigned_date',
    ]
    filterset_fields = ['user__username']
    ordering_fields = '__all__'
    queryset = AssignedVehicle.objects.all()
    # lookup_field = 'pk'

    def unasigned_user_vehicle(self, request):
        try:
            assigned = self.get_queryset().get(user=request.data['user'], vehicle=request.data['vehicle'])
            if assigned:
                assigned.delete()
            return DoneResponse(**codes.USER_VEHICLE_DELETED)
        except AssignedVehicle.DoesNotExist:
            return DoneResponse(**codes.USER_VEHICLE_NOT_FOUND)
