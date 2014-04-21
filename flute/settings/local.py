from __future__ import absolute_import
from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'genos_flute',
        'USER': 'genos_flute',
        'PASSWORD': 'genos_flute',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}
