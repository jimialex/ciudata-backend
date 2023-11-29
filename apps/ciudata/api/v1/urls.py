# -*- coding: utf-8 -*-

from django.urls import path
from apps.ciudata.api.v1.views.route import *
from apps.ciudata.api.v1.views import (ConversorApiView, UsersViewSet,
                                       VehiclesViewSet)


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
    path(  # Users detail
        'users/<username>/',
        UsersViewSet.as_view({
            'get': 'retrieve'
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
        VehiclesViewSet.as_view({
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
    # >> Assigned Routes
    path(  # Assigned Routes List & Create
        'assigned-routes/',
        AssignedRouteViewSet.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='assigned-route-create-list',
    ),
    path(  # Assigned Routes Update, Retieve & Delete
        'assigned-routes/<slug>/',
        AssignedRouteViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='assigned-route-detail-update-delete',
    ),

]
