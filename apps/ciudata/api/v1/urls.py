# -*- coding: utf-8 -*-

from django.urls import path
from apps.ciudata.api.v1.views.route import *
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
    # >> Areas
    path(  # Areas List & Create
        'areas/',
        AreasViewSet.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='area-create-list',
    ),
    path(  # Areas Update, Retieve & Delete
        'areas/<slug>/',
        AreasViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='area-detail-update-delete',
    ),
    # >> Routes
    path(  # Routes List & Create
        'routes/',
        RoutesViewSet.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='route-create-list',
    ),
    path(  # Routes Update, Retieve & Delete
        'routes/<slug>/',
        RoutesViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='route-detail-update-delete',
    ),

]
