# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.contrib.api.viewsets import (PermissionViewSet,
                                       ModelCreateListViewSet,
                                       MixinPagination, ModelRetrieveUpdateDeleteListViewSet)
from apps.ciudata.api.v1.serializers.route import *
from apps.ciudata.models.route import *
from apps.contrib.api.responses import DoneResponse
from apps.ciudata.api.v1 import codes
CREATED = "CREATED"


class AreasViewSet(PermissionViewSet, ModelCreateListViewSet, ModelRetrieveUpdateDeleteListViewSet):
    """Contains all users endpoints."""

    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']
    ordering_fields = '__all__'
    lookup_field = 'slug'
    queryset = Area.objects.filter(db_status=CREATED)
    pagination_class = MixinPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.AREA_DELETED)


class RoutesViewSet(PermissionViewSet, ModelCreateListViewSet, ModelRetrieveUpdateDeleteListViewSet):
    """Contains all users endpoints."""

    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
    search_fields = [
        'name', 'area__name',
    ]
    filterset_fields = ['name']
    ordering_fields = '__all__'
    queryset = Route.objects.filter(db_status=CREATED)
    pagination_class = MixinPagination
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.ROUTE_DELETED)
