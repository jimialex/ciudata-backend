# -*- coding: utf-8 -*-

from django.urls import path, include

app_name = 'ciudata'
urlpatterns = [
    path('v1/', include('apps.ciudata.api.v1.urls', namespace='v1')),
]
