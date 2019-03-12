from decouple import config, Csv

from .base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', cast=int, default=''),
    }
}

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_DB = config('REDIS_DB')
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

PROXY_HOST = config('PROXY_HOST')
PROXY_PORT = config('PROXY_PORT', cast=int)
PROXY_USERNAME = config('PROXY_USERNAME')
PROXY_PASSWORD = config('PROXY_PASSWORD')

# Default API ID and API HASH
API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')

# Coinpayments
COINPAYMENTS_API_KEY = config('COINPAYMENTS_API_KEY')
COINPAYMENTS_API_SECRET = config('COINPAYMENTS_API_SECRET')
COINPAYMENTS_IPN_URL = config('COINPAYMENTS_IPN_URL')
COINPAYMENTS_IPN_SECRET = config('COINPAYMENTS_IPN_SECRET')
COINPAYMENTS_MERCHANT_ID = config('COINPAYMENTS_MERCHANT_ID')

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', cast=bool)
