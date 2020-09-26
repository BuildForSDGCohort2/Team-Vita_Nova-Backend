from .base import *

from dj_database_url import parse as db_url
from datetime import timedelta


DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': config('DATABASE_URL', default='postgres:///vitaNova_db', cast=db_url),
}
