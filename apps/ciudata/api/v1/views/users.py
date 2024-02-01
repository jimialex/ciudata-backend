# -*- coding: utf-8 -*-
from rest_framework import status
from apps.contrib.api.responses import Response
from apps.ciudata.api.v1 import codes

from apps.contrib.api.viewsets import (BaseViewset, PermissionModelViewSet)
from apps.ciudata.api.v1.serializers.users import UsersSerializer, UsersResponseSerializer
from apps.accounts.models.user import User
from apps.ciudata.models.vehicle import AssignedVehicle


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
        if instance.assigned_vehicle.exists():
            assigned = instance.assigned_vehicle.first()
            assignement = AssignedVehicle.objects.get(pk=assigned.id)
            assignement.delete()
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        new_user = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(UsersResponseSerializer(new_user).data)

    def perform_update(self, serializer):
        return serializer.save()
