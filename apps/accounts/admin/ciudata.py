# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.ciudata.models import *


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """Defines the Area admin behaviour."""

    list_display = (
        'name',
        'geofence',
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Defines the Route admin behaviour."""

    list_display = (
        'name',
        'area',
        'db_status',
        # 'geo_route',
    )


@admin.register(AssignedRoute)
class AssignedRouteAdmin(admin.ModelAdmin):
    """Defines the Assigned Route admin behaviour."""

    list_display = (
        'user',
        'route',
        'assigned_detail',
        'assigned_date',
        'status',
        'completed_detail',
        'completed_date',
        'geo_route',
        'metadata',
    )
    list_editable = [
        'status'
    ]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Defines the Vehicle admin behaviour."""

    list_display = (
        'plate',
        'brand',
        'model',
        'detail',
        'photo',
        'metadata',
    )


@admin.register(AssignedVehicle)
class AssignedVehicleAdmin(admin.ModelAdmin):
    """Defines the Assigned Vehicle admin behaviour."""

    list_display = (
        'user',
        'vehicle',
        'detail',
        'assigned_date',
        'metadata',
    )


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    """Defines the Tracking admin behaviour."""

    list_display = (
        'assigned_route',
        'datetime',
        'lat',
        'lng',
    )
