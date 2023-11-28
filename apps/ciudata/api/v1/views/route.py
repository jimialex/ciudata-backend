# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.contrib.api.viewsets import (PermissionViewSet,
                                       ModelCreateListViewSet,
                                       MixinPagination, ModelRetrieveUpdateDeleteListViewSet)
from apps.ciudata.api.v1.serializers.vehicle import VehicleSerializer
from apps.ciudata.models.vehicle import *
from apps.contrib.api.responses import DoneResponse
from apps.ciudata.api.v1 import codes
from django.core.exceptions import ObjectDoesNotExist
CREATED = "CREATED"


class VehiclesViewSet(PermissionViewSet, ModelCreateListViewSet):
    """Contains all users endpoints."""

    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
    search_fields = [
        'plate', 'brand', 'model',
    ]
    filterset_fields = ['plate']
    ordering_fields = '__all__'
    queryset = Vehicle.objects.filter(db_status=CREATED)
    pagination_class = MixinPagination


class VehicleViewSet(PermissionViewSet, ModelRetrieveUpdateDeleteListViewSet):
    """Contains all users endpoints."""

    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    queryset = Vehicle.objects.filter(db_status=CREATED)
    lookup_field = 'slug'
    pagination_class = MixinPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.VEHICLE_DELETED)
