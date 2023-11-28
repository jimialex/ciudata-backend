# -*- coding: utf-8 -*-

from django.urls import path
from apps.ciudata.api.v1.views import (ConversorApiView, UsersViewSet,
                                       VehiclesViewSet, VehicleViewSet)


app_name = 'ciudata'
urlpatterns = [
    # >> Utils
    path(
        'conversor/',
        ConversorApiView.as_view(),
        name='conversor',
    ),
    # >> Users
    path(  # Users List
        'users/',
        UsersViewSet.as_view({
            'get': 'list'
        }),
        name='conversor',
    ),
    # >> Vehicles
    path(  # Vehicles List & Create
        'vehicles/',
        VehiclesViewSet.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='conversor',
    ),
    path(  # Vehicles Update, Retieve & Delete
        'vehicles/<slug>/',
        VehicleViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='conversor',
    ),
]
