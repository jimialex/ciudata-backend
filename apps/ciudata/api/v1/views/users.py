# -*- coding: utf-8 -*-

from apps.contrib.api.viewsets import (BaseViewset)
from apps.ciudata.api.v1.serializers.users import UsersSerializer
from apps.accounts.models.user import User


class UsersViewSet(BaseViewset):
    """Contains all users endpoints."""

    serializer_class = UsersSerializer
    response_serializer_class = UsersSerializer
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
    lookup_field = 'username'
