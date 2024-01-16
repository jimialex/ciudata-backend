# -*- coding: utf-8 -*-
from rest_framework import status
from apps.contrib.api.responses import Response
from apps.ciudata.api.v1 import codes

from apps.contrib.api.viewsets import (BaseViewset, PermissionModelViewSet)
from apps.ciudata.api.v1.serializers.users import UsersSerializer, UsersResponseSerializer
from apps.accounts.models.user import User


class UsersViewSet(BaseViewset):
    """Contains all users endpoints."""

    serializer_class = UsersSerializer
    response_serializer_class = UsersResponseSerializer
    search_fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'groups__name',
    ]
    filterset_fields = ['groups']
    ordering_fields = '__all__'
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        # instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
