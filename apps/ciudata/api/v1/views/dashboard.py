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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {
            "area": serializer.data,
            "total_distance": self.get_total_distance(instance),
            "total_distance_tours": self.get_total_distance_tours(instance),
            "total_time_tour": self.get_total_time_tour_from_metadata(instance)[0],
            "total_average_speed": self.get_total_average_speed_km_hours(instance),
            "user_most_tour": self.get_user_and_vehicle_most_tour(instance)[0],
            "vehicle_most_record": self.get_user_and_vehicle_most_tour(instance)[1],
            "route_most_record": self.get_route_most_record(instance),
            "route_less_record": self.get_route_less_record(instance),
            "routes": self.get_routes_for_area(instance),
        }

        return Response(data)

    def get_routes_for_area(self, area):
        assigneds = AssignedRoute.objects.filter(route__area=area).distinct()
        array = []
        for assigned in assigneds:
            if assigned.route not in array:
                array.append(assigned.route)
        routes = RouteSerializer(array, many=True).data
        return routes

    def get_total_distance(self, area):
        """Este metodo realiza la suma de todas las distancias que se encuentra en metadata
        dentro del modelo assigned_route, el cual esta relaciondo con area dentro de la relacion
        con el modelo Route

        """
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
        return round(sum, 2)

    def get_total_distance_tours(self, area):
        """Este methodo calcula el total de la distancia recorrida de una ruta
        lo hace en base a las rutas-asignadas, sumando el campo traking_assigned_route
        que pertenece al modelo Tracking"""
        routes = area.route_area.all()
        sum = 0
        for route in routes:
            assigneds = route.route_assigned.all().filter(status=COMPLETED)
            sum = sum + self.sum_tracking_tours(assigneds)
        return round(sum, 2)

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
        return round(sum, 2)

    def get_total_time_tour_from_metadata(self, area):
        routes = area.route_area.all()
        sum = timedelta()
        for route in routes:
            assigneds = route.route_assigned.all().filter(status=COMPLETED)
            sum = sum + self.get_sum_tracking_time_from_metadata(assigneds)

        days, seconds = divmod(sum.total_seconds(), 86400)  # Segundos en un día
        hours, remaining_seconds = divmod(seconds, 3600)  # Segundos en una hora
        minutes, seconds = divmod(remaining_seconds, 60)  # Segundos en un minuto
        data = {
            "days": int(days),
            "hours": int(hours),
            "minutes": int(minutes),
            "seconds": int(seconds),
        }
        return data, sum

    def get_sum_tracking_time_from_metadata(self, assigneds):
        """En base a una lista de assigned_routes se suma todos los time_tracking
            que se encuentra dentro de metadata
            Tomar en cuenta que time_trackin es un array que se debe sumar y esa suma total 
            el la que se suma con los demas time_tracking de la lista assigned_routes.

        Returns:
            time: total_time
        """

        total_time = timedelta()
        for assigned in assigneds:
            if 'time_tracking' in assigned.metadata:
                time_array = assigned.metadata['time_tracking']

                for time_str in time_array:
                    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
                    total_time += timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)

        return total_time

    def get_total_average_speed_km_hours(self, area):
        total_distance_km = self.get_total_distance(area) / 1000  # distancia en Km.
        total_time = self.get_total_time_tour_from_metadata(area)[1]
        hours = (total_time.total_seconds() / 3600)  # Segundos en una hora
        if hours > 0:
            return round((total_distance_km / hours), 2)
        return 0

    def get_user_and_vehicle_most_tour(self, area):
        assigneds = AssignedRoute.objects.filter(route__area=area).filter(status=COMPLETED)
        assigned = assigneds.annotate(user_count=Count('user')).order_by('-user_count').first()
        if assigned is not None:
            user = assigned.user
            vehicle_assigned = user.assigned_vehicle.all().first()
            vehicle = f"{vehicle_assigned.vehicle.plate} - {vehicle_assigned.vehicle.brand}"
            return user.get_fullname, vehicle
        return "Sin conductor", "Sin vehículo"

    def get_route_most_record(self, area):
        route = area.route_area.annotate(amount=Count('route_assigned')).order_by('-amount').first()
        return {"slug": route.slug, "name": route.name, "amount": route.amount} if route else None

    def get_route_less_record(self, area):
        route = area.route_area.annotate(amount=Count('route_assigned')).order_by('amount').first()
        return {"slug": route.slug, "name": route.name, "amount": route.amount} if route else None

    def get_total_time_tour(self, area):  # POR BORRAR
        # TODO: este metodo debe ser borrado cuando ya no se use el modelo Tracking para los recorridos de rutas asignadas
        routes = area.route_area.all()
        sum = timedelta()
        for route in routes:
            assigneds = route.route_assigned.all().filter(status=COMPLETED)
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

    def get_sum_tracking_time(self, assigneds):  # POR BORRAR
        # TODO: este metodo debe ser borrado cuando ya no se use el modelo Tracking para los recorridos de rutas asignadas

        total_time = timedelta()
        for assigned in assigneds:
            if assigned.traking_assigned_route.exists():
                trackings = assigned.traking_assigned_route.all().values_list('datetime')
                first_datetime = datetime.fromisoformat(trackings.first()[0].strftime("%Y-%m-%d %H:%M:%S"))
                last_datetime = datetime.fromisoformat(trackings.last()[0].strftime("%Y-%m-%d %H:%M:%S"))
                time_difference = last_datetime - first_datetime
                total_time = total_time + time_difference
        return total_time
