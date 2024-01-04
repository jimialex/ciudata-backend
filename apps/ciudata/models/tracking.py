# -*- coding: utf-8 -*-

from django.db import models

from apps.contrib.models.mixins import *
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


class Tracking(TimeStampedModelMixin):
    """ This class is to Tracking model"""

    assigned_route = models.ForeignKey(
        'AssignedRoute',
        verbose_name=_('Ruta asignada'),
        related_name="traking_assigned_route",
        on_delete=models.CASCADE,
    )

    datetime = models.DateTimeField(
        verbose_name=_('Fecha y hora'),
        help_text=_('Fecha y hora del punto GPS captado en el trackeo'),
    )

    lat = models.FloatField(
        verbose_name=_('Latitud'),
    )

    lng = models.FloatField(
        verbose_name=_('Longitud'),
    )

    def __str__(self):
        return f"{self.assigned_route} - {self.datetime}"

    class Meta:
        db_table = 'tracking'
        verbose_name = _('Trackeo')
        verbose_name_plural = _('Trackeos')
        app_label = 'ciudata'
        ordering = ["-created_at"]
