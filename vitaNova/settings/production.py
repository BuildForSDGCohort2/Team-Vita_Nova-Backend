from .base import *
from decouple import config

DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True
CONN_MAX_AGE = None

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('vitaNova_db'),
        'USER': config('kelly'),
        'PASSWORD': config('iseT<1290'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
