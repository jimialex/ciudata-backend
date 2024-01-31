from rest_framework import serializers

from apps.accounts.models import User
from apps.ciudata.models import Area, Route, AssignedRoute, COMPLETED
from apps.ciudata.api.v1.serializers import AreaSerializer


class SimpleAssignedRouteSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()

    def get_user_fullname(self, obj):
        return obj.user.get_fullname

    class Meta:
        model = AssignedRoute
        fields = [
            'id',
            'slug',
            'user_fullname',
            'status',
            'assigned_date',
            'completed_date',
        ]


class SimpleDashboardRouteSerializer(serializers.ModelSerializer):
    # area = AreaSerializer()
    area = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    last_user_assigned = serializers.SerializerMethodField()
    last_date_tours = serializers.SerializerMethodField()
    number_of_tours = serializers.SerializerMethodField()

    def get_assignments(self, obj):
        if obj.route_assigned.exists():
            assigned = obj.route_assigned.all()
            return SimpleAssignedRouteSerializer(assigned, many=True).data
        return {}

    def get_last_user_assigned(self, obj):
        if obj.route_assigned.exists():
            assigned = obj.route_assigned.all().order_by('created_at').last()
            return assigned.user.get_fullname
        return None

    def get_last_date_tours(self, obj):
        if obj.route_assigned.exists():
            assigned = obj.route_assigned.filter(status=COMPLETED).order_by('created_at').last()
            return assigned.completed_date if (assigned is not None) else None
        return None

    def get_number_of_tours(self, obj):
        if obj.route_assigned.exists():
            return obj.route_assigned.filter(status=COMPLETED).count()
        return 0

    def get_status(self, obj):
        if obj.route_assigned.exists():
            return obj.route_assigned.first().status
        return None

    def get_area(self, obj):
        if obj.area:
            return obj.area.name
        return None

    class Meta:
        model = Route
        fields = [
            'id',
            'slug',
            'name',
            'status',
            'number_of_tours',
            'last_date_tours',
            'last_user_assigned',
            'area',
            'metadata',
            'assignments',
            'geo_route',
        ]
