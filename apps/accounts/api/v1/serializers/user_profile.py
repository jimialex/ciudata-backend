# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url')
    has_password = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()  # serializers.ListField(child=serializers.CharField(max_length=255))

    def get_has_password(self, user):
        return user.has_usable_password()

    def get_groups(self, user):
        if user.groups.exists():
            return [group.name for group in user.groups.all()]
        else:
            return []

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'photo',
            'lang',
            'is_active',
            'has_password',
            'groups',
        )
        read_only_fields = fields
