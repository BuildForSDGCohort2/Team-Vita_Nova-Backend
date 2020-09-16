from .base import *

DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True
CONN_MAX_AGE = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vitaNova_db',
        'USER': 'kelly',
        'PASSWORD': 'iseT<1290',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
