# -*- coding: utf-8 -*-

from django.urls import path
from apps.ciudata.api.v1.views import ConversorApiView, UsersViewSet


app_name = 'ciudata'
urlpatterns = [
    # >> Utils
    path(
        'conversor/',
        ConversorApiView.as_view(),
        name='conversor',
    ),
    # >> Users
    path(
        'users/',
        UsersViewSet.as_view({
            'get': 'list'
        }),
        name='conversor',
    ),
]
