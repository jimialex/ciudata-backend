# -*- coding: utf-8 -*-

# from rest_framework.response import Response
# from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.contrib.api.viewsets import (PermissionViewSet,
                                       ModelListViewSet, MixinPagination)
from apps.ciudata.api.v1.serializers.users import UsersSerializer
from apps.accounts.models.user import User


class UsersViewSet(PermissionViewSet, ModelListViewSet):
    """Contains all users endpoints."""

    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
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
    queryset = User.objects.all()
    pagination_class = MixinPagination
