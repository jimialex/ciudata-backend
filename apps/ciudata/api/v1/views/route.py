# -*- coding: utf-8 -*-
from rest_framework import status

from django.db.models import Q
from apps.contrib.api.viewsets import (BaseViewset, )
from apps.contrib.api.responses import DoneResponse, Response
from apps.ciudata.api.v1.serializers.route import *
from apps.ciudata.api.v1.serializers.assignations import *
from apps.ciudata.models.route import *
from apps.ciudata.api.v1 import codes
CREATED = "CREATED"


class AreasViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = AreaSerializer
    response_serializer_class = AreaSerializer
    search_fields = ['name']
    filterset_fields = ['name']
    ordering_fields = '__all__'
    lookup_field = 'slug'
    queryset = Area.objects.filter(db_status=CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.AREA_DELETED)


class RoutesViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = RouteSerializer
    response_serializer_class = RouteResponseSerializer
    search_fields = ['name', 'area__name', 'route__slug']
    filterset_fields = ['name', 'route_assigned__status', 'route__slug']
    ordering_fields = '__all__'
    queryset = Route.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.ROUTE_DELETED)

    def get_queryset(self):
        # queryset = super(RoutesViewSet, self).get_queryset()
        queryset = super().get_queryset().distinct()

        # Apply queryparams filtering
        for key, value in self.request.query_params.items():
            queryset = queryset.filter(Q(**{key: value}))

        return queryset

    def list_unassigned(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = Route.objects.filter(db_status=CREATED)

        queryset = queryset.exclude(route_assigned__status=ASSIGNED)
        # queryset = super().get_queryset().exclude(route_assigned__status=ASSIGNED)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AssignedRouteViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = AssignedRouteSerializer
    response_serializer_class = AssignedRouteCompleteSerializer
    search_fields = [
        'user__username', 'user__first_name',
        'user__last_name', 'route__name', 'route__slug'
    ]
    filterset_fields = ['status', 'route__slug']
    queryset = AssignedRoute.objects.filter()
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.ROUTE_DELETED)

    def create(self, request, *args, **kwargs):
        serializer = AssignedRouteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
