from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, F, Sum, OuterRef, Subquery
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import TruncDay, ExtractWeekDay

from apps.contrib.api.viewsets import PermissionModelViewSet
from apps.ciudata.models import AssignedRoute, Route
from apps.ciudata.models import CREATED, COMPLETED
from datetime import datetime, timedelta
from functools import reduce
from collections import Counter
# from django.utils.dateparse import parse_datetime


class DateUndefinedException(Exception):
    pass


class DatedViewSet(object):
    date_format = "%Y-%m-%d"

    def get_dates(self):
        import pytz
        req = self.request.GET
        if 'init_date' in req and 'final_date' in req:
            init_date = datetime.strptime(req['init_date'], self.date_format)
            final_date = datetime.strptime(req['final_date'], self.date_format)

            # final_date = final_date + timedelta(days=1)
            init_date = init_date.replace(tzinfo=(pytz.timezone('America/La_Paz')))
            final_date = final_date.replace(tzinfo=(pytz.timezone('America/La_Paz')))
            final_date = final_date + timedelta(hours=23) + timedelta(minutes=59) + timedelta(seconds=59)

            return (init_date, final_date)
        else:
            raise (DateUndefinedException)

    def get_routes_travled(self):
        try:
            dates = self.get_dates()
            routes_travled = AssignedRoute.objects.filter(
                status=COMPLETED,
                completed_date__range=dates
            )
        except DateUndefinedException:
            routes_travled = AssignedRoute.objects.filter(status=COMPLETED)
        return routes_travled.order_by('id')

    def get_items(self):
        pass
        """
        try:
            dates = self.get_dates()
            items = Item.objects.filter(
                product__company=self.get_company(),
                transaction__creation_date__range=dates
            )
        except DateUndefinedException:
            items = Item.objects.filter(
                product__company=self.get_company()
            )
        return items
        """
