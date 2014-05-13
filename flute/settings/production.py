from __future__ import absolute_import
from .base import *

import json
from django.core.exceptions import ImproperlyConfigured


def get_secret():
    try:
        with open(join(DJANGO_ROOT, "serverconf.json")) as conf_file:
            return json.load(conf_file)
    except KeyError:
        raise ImproperlyConfigured("Create a proper serverconf.json")


SERVER_CONF = get_secret()
ALLOWED_HOSTS = ["flute.genosmus.com"]

SECRET_KEY = SERVER_CONF['secret-key']

STATIC_ROOT = '/home/genos/webapps/flute_static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'genos_flute',
        'USER': 'genos_flute',
        'PASSWORD': SERVER_CONF['db-password'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}
