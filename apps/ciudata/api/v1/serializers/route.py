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
            'metadata',
        ]


class RouteResponseSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    status = serializers.SerializerMethodField()
    route_assigned = serializers.SerializerMethodField()

    def get_route_assigned(self, obj):
        if obj.route_assigned.exists():
            assigned = obj.route_assigned.filter(status="ASSIGNED").values('user__username', 'assigned_date')
            return assigned
        return None

    def get_status(self, obj):
        if obj.route_assigned.exists():
            return obj.route_assigned.first().status
        return None

    class Meta:
        model = Route
        fields = [
            'id',
            'slug',
            'name',
            'status',
            'metadata',
            'route_assigned',
            'area',
            'geo_route',
        ]
