# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.accounts.api.v1.serializers.user import UserUpdateSerializer, UserCreateSerializer
from apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from apps.contrib.api.viewsets import PermissionViewSet
from apps.accounts.services.user import UserService
from apps.accounts.models.user import User


class ProfileViewSet(PermissionViewSet):
    """Contains all accounts endpoints."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        """Returns user profile."""
        profile = UserProfileSerializer(request.user).data
        return Response(profile)

    def update_profile(self, request):
        """Updates user profile."""
        serializer = UserUpdateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        UserService.update_profile(request.user, serializer.validated_data)

        request.user.refresh_from_db()
        return Response(self.get_serializer(request.user).data)

    def create_profile(self, request, *args, **kwargs):
        """Crete new user"""

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = UserService.register_new_user(serializer.validated_data, is_active=True)
        return Response(self.get_serializer(new_user).data, status=status.HTTP_200_OK)
