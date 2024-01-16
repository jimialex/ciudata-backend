# -*- coding: utf-8 -*-

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
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


class ModelRetrieveUpdateDeleteListViewSet(  # noqa: WPS215
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
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


# class BaseViewset(PermissionViewSet, ModelCreateListViewSet, ModelRetrieveUpdateDeleteListViewSet):
class BaseViewset(ModelCreateListViewSet,
                  ModelRetrieveUpdateDeleteListViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = MixinPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       DjangoFilterBackend]
    response_serializer_class = None

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT"]:
            return self.serializer_class(*args, **kwargs)
        elif self.request.method in ["GET", "DELETE"]:
            return self.response_serializer_class(*args, **kwargs)
        else:
            raise ValidationError("Método HTTP no soportado")
