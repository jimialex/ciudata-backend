# -*- coding: utf-8 -*-

from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status, pagination
from rest_framework.response import Response


class PermissionlMixin(object):
    """Views permission mixin.

    Mixed permission base model allowing for action level
    permission control. Subclasses may define their permissions
    by creating a 'permission_classes_by_action' variable.

    Example:
    permissions_by_action = {'list': [AllowAny], 'create': [IsAdminUser]}

    """

    permissions_by_action = {}

    def get_permissions(self):
        """Returns permissions calculation."""
        try:
            return [permission() for permission in self.permissions_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class ModelListViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list method with permissions."""


class ModelUpdateListViewSet(  # noqa: WPS215
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and update methods with permissions."""


class ModelRetrieveListViewSet(  # noqa: WPS215
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and retrieve methods with permissions."""


class ModelRetrieveUpdateListViewSet(  # noqa: WPS215
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables retrieve and update methods with permissions."""


class ModelCreateRetrieveListViewSet(  # noqa: WPS215
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list, create and retrieve methods with permissions."""


class ModelCreateListViewSet(  # noqa: WPS215
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Enables list and createe methods with permissions."""


class PermissionModelViewSet(PermissionlMixin, ModelViewSet):
    """Enables all modeel methods with permissions."""


class PermissionViewSet(PermissionlMixin, GenericViewSet):
    """Enables standar view methods with permissions."""


class MixinPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    page_link_template = 'page={page_number}'

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "page_number": self.page.number,
            "page_size": self.page.paginator.per_page,
            "results": data,
        })

    def set_page_size(self, size):
        self.page_size = size
