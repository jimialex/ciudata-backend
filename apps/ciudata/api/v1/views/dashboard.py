# -*- coding: utf-8 -*-
from rest_framework import status

from django.db.models import Q
from apps.contrib.api.viewsets import (BaseViewset, )
from apps.contrib.api.responses import DoneResponse, Response
from apps.ciudata.api.v1.serializers import *
from apps.ciudata.api.v1.serializers.assignations import *
from apps.ciudata.models.route import *
CREATED = "CREATED"


class DashboardRoutesViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = SimpleDashboardRouteSerializer
    response_serializer_class = SimpleDashboardRouteSerializer
    search_fields = ['name', 'area__name', 'route__slug', 'route_assigned__status']
    filterset_fields = ['name', 'route_assigned__status',]
    ordering_fields = ['id', 'created_at', 'route_assigned__assigned_date', 'route_assigned__completed_date']
    queryset = Route.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def get_queryset(self):
        # queryset = super(RoutesViewSet, self).get_queryset()
        queryset = super().get_queryset().distinct()

        # Apply queryparams filtering
        for key, value in self.request.query_params.items():
            queryset = queryset.filter(Q(**{key: value}))

        return queryset


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
