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


# Leave this commented, only use in an emergency ;-)
# DEBUG = True
# TEMPLATE_DEBUG = DEBUG


SERVER_CONF = get_secret()
ALLOWED_HOSTS = ["flute.genosmus.com"]
SECRET_KEY = SERVER_CONF['secret-key']
STATIC_ROOT = '/home/genos/webapps/flute_static/'

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'genos'
EMAIL_HOST_PASSWORD = SERVER_CONF['email-password']
DEFAULT_FROM_EMAIL = 'genos@genosmus.com'
SERVER_EMAIL = 'genos@genosmus.com'

DEALER_PATH = "/home/genos/webapps/flute/flute"

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
