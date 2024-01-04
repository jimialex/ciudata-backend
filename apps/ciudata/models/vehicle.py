# -*- coding: utf-8 -*-

from django.db import models

from apps.contrib.models.mixins import *
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from apps.contrib.utils.strings import get_uuid


class Vehicle(TimeStampedModelMixin, Slug10ModelMixin, DeletionMixin):
    """ This class is to vehicle model"""
    plate = models.CharField(
        verbose_name=_('Placa'),
        max_length=8,
        unique=True,
    )

    brand = models.CharField(
        verbose_name=_('Marca'),
        max_length=150,
    )

    model = models.IntegerField(
        verbose_name=_('Modelo (año)'),
        blank=True, null=True,
    )

    detail = models.TextField(
        verbose_name=_('Detalle'),
        blank=True, null=True,
    )

    photo = ProcessedImageField(
        verbose_name=_('Fotografía'),
        upload_to='vehiculos/%Y%m%d',
        processors=[ResizeToFill(700, 700)],
        format='PNG',
        options={'quality': 90},
        blank=True, null=True,
    )

    metadata = JSONField(
        verbose_name=_('Metadata'),
        blank=True, null=True,
    )

    def __str__(self):
        return self.plate

    class Meta:
        db_table = 'vehicle'
        verbose_name = _('Vehículo')
        verbose_name_plural = _('Vehículos')
        app_label = 'ciudata'
        ordering = ["-created_at"]


class AssignedVehicle(TimeStampedModelMixin):
    """ This class is to vehicle assigned to user model"""
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='assigned_vehicle',
    )

    vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.CASCADE,
        related_name='conductor',
    )

    detail = models.TextField(
        verbose_name=_('Detalle'),
        blank=True, null=True,
    )

    assigned_date = models.DateField(
        verbose_name=_('Fecha asignación'),
        auto_now_add=True
    )

    metadata = JSONField(
        verbose_name=_('Metadata'),
        blank=True, null=True,
    )

    def __str__(self):
        return f"{self.user.username} {self.vehicle}"

    class Meta:
        db_table = 'asigned_vehicle'
        verbose_name = _('Vehículo asignado')
        verbose_name_plural = _('Vehículos asignados')
        app_label = 'ciudata'
        ordering = ["-created_at"]
