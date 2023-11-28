# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.contrib.utils.strings import get_uuid


class TimeStampedModelMixin(models.Model):
    """Timestamp extra field.

    An abstract base class model that provides self updating 'created' and 'modified' fields
    https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class UUIDModelMixin(models.Model):
    """An abstract base class model that provides an uuid field."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    """An abstract base class model that provides a slug field."""

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True


class Slug10ModelMixin(models.Model):
    """An abstract base class model that provides a slug field."""

    slug = models.SlugField(
        verbose_name=_("Slug"),
        default=get_uuid,
        db_index=True,
        unique=True,
    )

    class Meta:
        abstract = True


class UUIDPrimaryKeyModelMixin(models.Model):
    """An abstract base class model that provides an uuid field that is the primary key."""

    uuid = models.UUIDField(
        verbose_name='UUID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True

##############################################################################################
# Deletion mixin


CREATED = "CREATED"
DELETED = "DELETED"


class DeletionManager(models.Manager):

    def __init__(self, show_deleted):
        self.show_deleted = show_deleted
        return super(DeletionManager, self).__init__()

    def get_queryset(self):
        if self.show_deleted:
            queryset = super(DeletionManager, self).get_queryset()
        else:
            queryset = super(DeletionManager, self).get_queryset().filter(db_status=CREATED)
        return queryset


class DeletionMixin(models.Model):

    # @property
    # def objects(self):
    #     return DeletionManager(self.show_deleted)

    DB_STATUS_KINDS = (
        (CREATED, "Created"),
        (DELETED, "Deleted"),
    )

    db_status = models.CharField(
        verbose_name=_("Estado de existencia en la base de datos"),
        max_length=20,
        choices=DB_STATUS_KINDS,
        default=CREATED
    )

    def delete(self):
        self.db_status = DELETED
        self.save()

    class Meta:
        abstract = True
