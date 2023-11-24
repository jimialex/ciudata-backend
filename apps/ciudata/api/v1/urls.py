# -*- coding: utf-8 -*-

from django.urls import path
from apps.ciudata.api.v1.views import ConversorApiView


app_name = 'ciudata'
urlpatterns = [
    # >> Register
    path(
        'conversor/',
        ConversorApiView.as_view(),
        name='conversor',
    ),
]
