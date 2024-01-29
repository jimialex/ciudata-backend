#!/usr/bin/env python3

from rest_framework import serializers


class IncomeSerializer(serializers.Serializer):

    date = serializers.DateField()
    kind = serializers.CharField()
    detail = serializers.CharField()
    client = serializers.CharField()
    amount = serializers.FloatField()


class IncomeProductsSerializer(serializers.Serializer):

    date = serializers.DateField()
    kind = serializers.CharField()
    detail = serializers.CharField()
    client = serializers.CharField()
    amount = serializers.FloatField()


class OutcomeSerializer(serializers.Serializer):

    date = serializers.DateField()
    kind = serializers.CharField()
    detail = serializers.CharField()
    category = serializers.CharField()
    provider = serializers.CharField()
    amount = serializers.FloatField()


class RoutesTraveledSerializer(serializers.Serializer):

    title = serializers.CharField()
    initial_date = serializers.DateField()
    final_date = serializers.DateField()

    routes_travled = serializers.JSONField()

    # routes_travled = AssignedRouteSerializer()
    # class Meta:
    #     model = Company
    #     fields = [
    #         # "name",
    #         "owner_name",
    #     ]
