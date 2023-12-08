# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.accounts.api.v1.serializers.user_profile import (
    UserProfileSerializer,
)


class UsernameOrEmailSerializer(Serializer):
    """Serializer to get and validate email or user name."""
    user = serializers.CharField()


class LoginSerializer(UsernameOrEmailSerializer):
    """Serializer to extends some validation to UsernameOrEmailSerializer."""
    password = serializers.CharField(style={'input_type': 'password'})


# SERIALIZER: Nuevo Login usando SimpleJWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # refresh = self.get_token(self.user)
        # data['profile'] =UserProfileSerializer(self.user).data
        user_data = UserProfileSerializer(self.user).data
        new_data = dict(**data, **user_data)
        new_data['api_token'] = data['access']
        return new_data


class TokenVerifyResponseSerializer(Serializer):
    # No se esta usando en el view
    token = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def validate(self, attrs):
        return super().validate(attrs)
