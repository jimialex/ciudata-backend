# -*- coding: utf-8 -*-
from django.db.models import Count
from django.db.models import F, Max, Min
from rest_framework import status
from datetime import datetime, timedelta

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


class DashboardAreasViewSet(BaseViewset):
    """Contains all users endpoints."""
    serializer_class = DashboardAreaSerializer
    response_serializer_class = DashboardAreaStatisticsSerializer
    search_fields = ['name']
    filterset_fields = ['name']
    ordering_fields = ['id', 'created_at']
    queryset = Area.objects.filter(db_status=CREATED)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        print("\n\n\n Statistic area")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "area": serializer.data,
            "total_distance": self.get_total_distance(instance),
            "total_distance_tours": self.get_total_distance_tours(instance),
            "total_time_tour": self.get_total_time_tour(instance),
            "total_average_speed": self.get_total_average_speed(instance),
            "user_most_tour": self.get_user_most_tour(instance),
            "vehicle_most_record": self.get_vehicle_most_record(instance),
            "route_most_record": self.get_route_most_record(instance),
            "route_less_record": self.get_route_less_record(instance),
        }

        return Response(data)

    def get_total_distance(self, area):
        """This method returns total distnace in the area's routes """
        routes = area.route_area.all()
        sum = 0
        # TODO: optimizar este codigo
        for route in routes:
            if 'distance' in route.metadata:
                if type(route.metadata['distance']) in [float, int]:
                    sum = sum + route.metadata['distance']
                else:
                    route.metadata['distance'] = float(route.metadata['distance'])
                    route.save()
                    sum = sum + route.metadata['distance']
        return sum

    def get_total_distance_tours(self, area):
        """Este methodo calcula el total de la distancia recorrida de una ruta
        lo hace en base a las rutas-asignadas, sumando el campo traking_assigned_route
        que pertenece al modelo Tracking"""
        routes = area.route_area.all()
        sum = 0
        for route in routes:
            assigneds = route.route_assigned.all()
            sum = sum + self.sum_tracking_tours(assigneds)
        return sum

    def sum_tracking_tours(self, assigneds):
        """Retorna la suma de las rutas recorridas despues de la asignacion
        el trackeo se suma a partir del campo distance_tracking en metadata
        que esta en el modelo AssignedRoute

        El paramatro de ingreso assigneds es una lista de objetos
        de tipo AssignedRoute"""

        sum = 0
        for assigned in assigneds:
            if 'distance_tracking' in assigned.metadata:
                if type(assigned.metadata['distance_tracking']) in [float, int]:
                    sum = sum + assigned.metadata['distance_tracking']
                else:
                    assigned.metadata['distance_tracking'] = float(assigned.metadata['distance_tracking'])
                    assigned.save()
                    sum = sum + assigned.metadata['distance_tracking']
        return sum

    def get_total_time_tour(self, area):
        routes = area.route_area.all()
        sum = timedelta()
        for route in routes:
            assigneds = route.route_assigned.all()
            sum = sum + self.get_sum_tracking_time(assigneds)

        days, seconds = divmod(sum.total_seconds(), 86400)  # Segundos en un día
        hours, remaining_seconds = divmod(seconds, 3600)  # Segundos en una hora
        minutes, seconds = divmod(remaining_seconds, 60)  # Segundos en un minuto
        data = {
            "days": int(days),
            "hours": int(hours),
            "minutes": int(minutes),
            "seconds": int(seconds),
        }
        return data

    def get_sum_tracking_time(self, assigneds):
        total_time = timedelta()
        for assigned in assigneds:
            if assigned.traking_assigned_route.exists():
                trackings = assigned.traking_assigned_route.all().values_list('datetime')
                first_datetime = datetime.fromisoformat(trackings.first()[0].strftime("%Y-%m-%d %H:%M:%S"))
                last_datetime = datetime.fromisoformat(trackings.last()[0].strftime("%Y-%m-%d %H:%M:%S"))
                time_difference = last_datetime - first_datetime
                total_time = total_time + time_difference
        return total_time

    def get_total_average_speed(self, assigneds):
        pass

    def get_user_most_tour(self, assigneds):
        pass

    def get_vehicle_most_record(self, assigneds):
        pass

    def get_route_most_record(self, area):
        route = area.route_area.annotate(amount=Count('route_assigned')).order_by('-amount').first()
        return {"slug": route.slug, "name": route.name, "amount": route.amount} if route else None

    def get_route_less_record(self, area):
        route = area.route_area.annotate(amount=Count('route_assigned')).order_by('amount').first()
        return {"slug": route.slug, "name": route.name, "amount": route.amount} if route else None
