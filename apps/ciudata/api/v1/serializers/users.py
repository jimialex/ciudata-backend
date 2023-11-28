# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.accounts.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""

    photo = serializers.CharField(source='photo_url')
    groups = serializers.SerializerMethodField()  # serializers.ListField(child=serializers.CharField(max_length=255))

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
            'groups',
        )
        read_only_fields = fields
