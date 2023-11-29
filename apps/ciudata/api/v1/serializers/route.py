from rest_framework import serializers

from apps.ciudata.models import Area, Route

from apps.accounts.models import User


class UsersSimpleSerializer(serializers.ModelSerializer):
    """Helps to print the useer basic info."""
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
            'groups',
        )
        read_only_fields = fields


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'slug', 'name', 'geofence']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'id',
            'slug',
            'name',
            'area',
            'geo_route',
        ]


class RouteResponseSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Route
        fields = [
            'id',
            'slug',
            'name',
            'area',
            'geo_route',
        ]
