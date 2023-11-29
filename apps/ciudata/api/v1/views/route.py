# -*- coding: utf-8 -*-

from apps.contrib.api.viewsets import (BaseViewset, )
from apps.ciudata.api.v1.serializers.route import *
from apps.ciudata.api.v1.serializers.assignations import *
from apps.ciudata.models.route import *
from apps.contrib.api.responses import DoneResponse
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
    search_fields = ['name', 'area__name',]
    filterset_fields = ['name']
    ordering_fields = '__all__'
    queryset = Route.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.ROUTE_DELETED)


class AssignedRouteViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = AssignedRouteSerializer
    response_serializer_class = AssignedRouteCompleteSerializer
    search_fields = [
        'user__username', 'user__first_name',
        'user__last_name', 'route__name',
    ]
    queryset = AssignedRoute.objects.filter()
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DoneResponse(**codes.ROUTE_DELETED)
