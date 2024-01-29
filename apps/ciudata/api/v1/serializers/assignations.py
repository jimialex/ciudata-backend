# Django & DRF
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from datetime import datetime

# Serializers
from apps.ciudata.api.v1.serializers.route import RouteSerializer, UsersSimpleSerializer

# Models
from apps.accounts.models import User
from apps.ciudata.models import (Area, Tracking, AssignedRoute,
                                 Route, ASSIGNED, COMPLETED)


class AssignedRouteCreateSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        route = data['route']
        if route.route_assigned.exists():
            # verificamos su la ruta asignada tiene alguna asignacion sin completar
            if (route.route_assigned.filter(status=ASSIGNED).exists()):
                raise serializers.ValidationError({'route': [_('Route is already assigned.')]})
        return data

    class Meta:
        model = AssignedRoute
        fields = [
            'slug',
            'user',
            'route',
            'assigned_detail',
            'assigned_date',
            'status',
            'completed_detail',
            'completed_date',
            'geo_route',
            'metadata',
        ]


class AssignedRouteSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = AssignedRoute
        fields = [
            'slug',
            'user',
            'route',
            'assigned_detail',
            'assigned_date',
            'status',
            'completed_detail',
            'completed_date',
            'geo_route',
            'metadata',
        ]


class AssignedRouteResponseSerializer(serializers.ModelSerializer):
    # user = UsersSimpleSerializer()
    route = RouteSerializer()

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'assigned_detail',
            'assigned_date',
            'status',
            'geo_route',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
        ]


class TrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracking
        fields = ['lat', 'lng', 'datetime', 'metadata']


class AssignedRouteCompleteSerializer(serializers.ModelSerializer):
    user = UsersSimpleSerializer()
    route = RouteSerializer()
    traking_assigned_route = serializers.SerializerMethodField()

    def get_traking_assigned_route(self, obj):
        """Return all points in traking for Assigned route"""
        if obj.traking_assigned_route is not None:
            points = obj.traking_assigned_route.all()
            return TrackingSerializer(points, many=True).data
        return {}

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'assigned_detail',
            'assigned_date',
            'status',
            'geo_route',
            'user',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
            'traking_assigned_route',
        ]


class AssignedRouteSimpleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = UsersSimpleSerializer()
    route = serializers.SerializerMethodField()

    def get_route(self, obj):
        return obj.route.name

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'route',
            'user',
            'assigned_date',
            'status',
        ]


class AssignedRouteReportSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    # user = UsersSimpleSerializer()
    route = RouteSerializer()
    traking_assigned_route = serializers.SerializerMethodField()
    initial_date = serializers.SerializerMethodField()
    final_date = serializers.SerializerMethodField()
    total_time = serializers.SerializerMethodField()
    ciudad = serializers.SerializerMethodField()

    def get_traking_assigned_route(self, obj):
        """Return all points in traking for Assigned route"""
        if obj.traking_assigned_route is not None:
            points = obj.traking_assigned_route.all()
            return TrackingSerializer(points, many=True).data
        return {}

    def get_initial_date(self, obj):
        try:
            # Obtener el primer punto de seguimiento directamente
            first = obj.traking_assigned_route.first()

            # Si existe un primer punto, formatear la fecha
            if first:
                date = first.datetime.strftime("%d-%m-%Y (%H:%M)")
                return date

            # Si no hay puntos de seguimiento, devolver None
            return None

        # Manejar la excepción de QuerySet vacío
        except obj.traking_assigned_route.model.DoesNotExist:
            return None

    def get_final_date(self, obj):
        try:
            # Obtener el último punto de seguimiento directamente
            last = obj.traking_assigned_route.last()

            # Si existe un último punto, formatear la fecha
            if last:
                date = last.datetime.strftime("%d-%m-%Y (%H:%M)")
                return date

            # Si no hay puntos de seguimiento, devolver None
            return None

        # Manejar la excepción de QuerySet vacío
        except obj.traking_assigned_route.model.DoesNotExist:
            return None

    def get_total_time(self, obj):
        initial_date = self.get_initial_date(obj)
        final_date = self.get_final_date(obj)

        if initial_date is not None and final_date is not None:
            try:
                initial_date = datetime.strptime(initial_date, "%d-%m-%Y (%H:%M)")
                final_date = datetime.strptime(final_date, "%d-%m-%Y (%H:%M)")
                total_time_delta = final_date - initial_date
                total_seconds = total_time_delta.total_seconds()
                total_hours = int(total_seconds // 3600)
                total_minutes = int((total_seconds % 3600) // 60)
                total_time_str = f"{total_hours:02d}:{total_minutes:02d}"
                return total_time_str  # Retorna el tiempo en formato HH:MM
            except ValueError:
                # Manejar el error si las fechas no tienen el formato esperado
                return None
        else:
            return None

    def get_user(slef, obj):
        if (obj.user.first_name and obj.user.last_name):
            return '{0} {1}'.format(obj.user.first_name, obj.user.last_name)
        return obj.user.username

    def get_ciudad(self, obj):
        return obj.route.area.name

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'assigned_detail',
            'assigned_date',
            'status',
            'geo_route',
            'user',
            'route',
            'metadata',
            'completed_detail',
            'completed_date',
            'traking_assigned_route',
            'initial_date',
            'final_date',
            'total_time',
            'ciudad',

        ]
