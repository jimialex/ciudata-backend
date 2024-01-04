# -*- coding: utf-8 -*-

from django.db import models

from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder

from apps.contrib.models.mixins import *


class Area(TimeStampedModelMixin, Slug10ModelMixin, DeletionMixin):
    """ This class is to Area model"""
    name = models.CharField(
        verbose_name=_('Nombre'),
        max_length=250,
    )

    geofence = JSONField(
        verbose_name=_('GEO-cerca'),
        help_text=_('Ingresar un array de jsons [{lat : --,lng : --}]'),
        blank=True, null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'area'
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')
        app_label = 'ciudata'


class Route(TimeStampedModelMixin, Slug10ModelMixin, DeletionMixin):
    """ This class is to Ruta model"""
    name = models.CharField(
        verbose_name=_('Nombre'),
        max_length=250,
    )

    area = models.ForeignKey(
        'Area',
        on_delete=models.CASCADE,
        related_name='route_area',
        blank=True, null=True,
    )

    geo_route = JSONField(
        verbose_name=_('Ruta GPS'),
        help_text=_('Ingresar un array de jsons [{lat : --,lng : --}]'),
        blank=True, null=True,
    )
    metadata = JSONField(
        encoder=DjangoJSONEncoder,
        verbose_name=_('Metadata'),
        blank=True, default=dict,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'route'
        verbose_name = _('Ruta')
        verbose_name_plural = _('Rutas')
        app_label = 'ciudata'
        ordering = ["-created_at"]


CREATED = "CREATED"
ASSIGNED = "ASSIGNED"
COMPLETED = "COMPLETED"
CANCELLED = "CANCELLED"


class AssignedRoute(TimeStampedModelMixin, Slug10ModelMixin):
    """ This class is to Assigned Route model"""
    STATUS_KINDS = (
        (ASSIGNED, "ASSIGNED"),
        (COMPLETED, "COMPLETED"),
        (CANCELLED, "CANCELLED"),
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='assigned_route',
    )

    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='route_assigned',
    )

    assigned_detail = models.TextField(
        verbose_name=_('Detalle de asignación de ruta'),
        blank=True, null=True,
    )

    assigned_date = models.DateField(
        verbose_name=_('Fecha asignación de ruta'),
        auto_now_add=True
    )

    status = models.CharField(
        verbose_name=_("Estado de asignación"),
        max_length=20,
        choices=STATUS_KINDS,
        default=ASSIGNED
    )

    completed_detail = models.TextField(
        verbose_name=_('Detalle de ruta completado'),
        blank=True, null=True,
    )

    completed_date = models.DateField(
        verbose_name=_('Fecha de ruta completado'),
        blank=True, null=True,
    )

    geo_route = JSONField(
        verbose_name=_('Ruta real completado'),
        help_text=_('Ingresar un array de jsons [{lat : --,lng : --}]'),
        blank=True, null=True,
    )

    metadata = JSONField(
        encoder=DjangoJSONEncoder,
        verbose_name=_('Metadata'),
        blank=True, null=True,
        default=dict,
    )

    def __str__(self):
        return f"{self.user.username} {self.route}"

    @property
    def get_traking(self):
        return self.traking_assigned_route.all()

    class Meta:
        db_table = 'asigned_route'
        verbose_name = _('Ruta asignada')
        verbose_name_plural = _('Rutas asignadas')
        app_label = 'ciudata'
        ordering = ["-created_at"]
