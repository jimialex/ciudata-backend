# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.ciudata.models import *


@admin.register(Area)
class Areadmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

    list_display = (
        'name',
        'geofence',
    )


@admin.register(Route)
class Routedmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

    list_display = (
        'name',
        'area',
        'geo_route',
    )


@admin.register(AssignedRoute)
class AssignedRoutedmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

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


@admin.register(Vehicle)
class Vehicledmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

    list_display = (
        'plate',
        'brand',
        'model',
        'detail',
        'photo',
        'metadata',
    )


@admin.register(AssignedVehicle)
class AssignedVehicledmin(admin.ModelAdmin):
    """Defines the phone device admin behaviour."""

    list_display = (
        'user',
        'vehicle',
        'detail',
        'assigned_date',
        'metadata',
    )
