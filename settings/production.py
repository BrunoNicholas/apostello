"""Settings used in production with ansible deploy."""
import os

from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']  # must define this

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 600,
    }
}

# cache templates in production
TEMPLATES[0]['OPTIONS']['loaders'] = [
    (
        'django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

STATIC_ROOT = '/webapps/apostello/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'apostello': {
            'level': 'WARNING',
            'handlers': ['opbeat'],
            'propagate': False,
        },
    },
}

if os.environ.get('OPBEAT_ORG_ID', None) is not None:
    INSTALLED_APPS += ['opbeat.contrib.django', ]

    MIDDLEWARE_CLASSES = [
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    ] + MIDDLEWARE_CLASSES

    LOGGING['handlers']['opbeat'] = {
        'level': 'WARNING',
        'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
    }
    LOGGING['loggers']['opbeat.errors'] = {
        'level': 'ERROR',
        'handlers': ['console'],
        'propagate': False,
    }
