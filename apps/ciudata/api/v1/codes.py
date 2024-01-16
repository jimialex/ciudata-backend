# -*- encoding:utf-8 -*-

from django.utils.translation import gettext_lazy as _
from rest_framework import status


# ~ ERRORS
# --------------------------------------------

OBJECT_NOT_FOUND = {
    "code": "object_not_found",
    "detail": _("Item no encontrado"),
}

VEHICLE_NOT_FOUND = {
    "code": "vehicle_not_found",
    "detail": _("El vehículo no existe"),
}

PRODUCT_NOT_FOUND = {
    "code": "product_not_found",
    "detail": _("Producto no encontrado"),
}

CLIENT_NOT_FOUND = {
    "code": "client_not_found",
    "detail": _("Cliente no encontrado"),
}

PROVIDER_NOT_FOUND = {
    "code": "provider_not_found",
    "detail": _("Proveedor no encontrado"),
}

EMPLOYEE_NOT_FOUND = {
    "code": "employee_not_found",
    "detail": _("Empleado no encontrado"),
}

RESOURCE_NOT_FOUND = {
    "code": "resource_not_found",
    "detail": _("Recurso no encontrado"),
}

TRANSACTION_NOT_FOUND = {
    "code": "transaction_not_found",
    "detail": _("Transacción no encontrada"),
}
INVALID_DATE_FORMAT = {
    "code": "invalid_date_format",
    "detail": _("Formato de fecha inválido"),
}


# ~ SUCCESS
# --------------------------------------------
PASSWORD_UPDATED = {
    "code": "password_updated",
    "detail": _("Contraseña actualizada con éxito"),
    "status": status.HTTP_201_CREATED
}

USER_DELETED = {
    "code": "user_deleted",
    "detail": _("Usuario Eliminado"),
    "status": status.HTTP_204_NO_CONTENT
}

VEHICLE_DELETED = {
    "code": "vehicle_deleted",
    "detail": _("Vehículo Eliminado"),
}
ROUTE_DELETED = {
    "code": "route_deleted",
    "detail": _("Ruta Eliminada"),
}
AREA_DELETED = {
    "code": "area_deleted",
    "detail": _("AREA Eliminada"),
}

CLIENT_DELETED = {
    "code": "client_deleted",
    "detail": _("Cliente Eliminado"),
}

NO_PREVIOUS_TRANSACTION = {
    "code": "no_previous_transaction",
    "detail": _("No existe transacción previa"),
}

TOKEN_CREATED = {
    "code": "token_created",
    "detail": _("Token de invitación creado"),
}

JOINED_COMPANY = {
    "code": "joined_company",
    "detail": _("Unido a la empresa"),
}


def server_error(err): return {"code": "server error", "detail": "{0}".format(err)}
