# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _


def api_code(code, message):
    """Returns a formatted API error."""
    return {
        'code': code,
        'message': _(message),
    }
