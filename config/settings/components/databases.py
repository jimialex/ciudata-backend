# -*- coding: utf-8 -*-

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
from config.settings.components import env

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='ciudata'),
        'USER': env('POSTGRES_USER', default='ciudata'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='11002299338844775566'),
        'HOST': env('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': env('POSTGRES_CONN_MAX_AGE', default=60),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    },
}
