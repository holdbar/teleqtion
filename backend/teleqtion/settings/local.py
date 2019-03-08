from .base import *


SECRET_KEY = '^lp2@0n-hl2%xq-w@xqe9v_z+ce248^#$(xich3yw7o3tmajjw'

DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '3'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + REDIS_DB

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

PROXY_HOST = 'zproxy.lum-superproxy.io'
PROXY_PORT = 22225
PROXY_USERNAME = 'lum-customer-hl_e909ad89-zone-static'
PROXY_PASSWORD = 'hl8gbyb0q37l'

# Default API ID and API HASH
API_ID = 682122
API_HASH = '97dfc2f618ce1b0ac317a25c59fa5666'

# Coinpayments
COINPAYMENTS_API_KEY = '59df620a69bed14360b9e05ddf0f7af04ccc1c27cc507a9c55b0f31b1feaf262'
COINPAYMENTS_API_SECRET = '78275bdCBf3954c1C28d236782d815b971570e985bc2d34AC97e2efed881F8A9'
COINPAYMENTS_IPN_URL = 'https://teleqtion.com/api/v1/payments/crypto/ipn/'
COINPAYMENTS_IPN_SECRET = '392nskne1c13vnld9*3d924lk598ao40'
COINPAYMENTS_MERCHANT_ID = 'b01331f0e1274763f55ea1069d055e5d'

COINMARKETCAP_API_KEY = 'b7e91288-d47a-4e0f-8a4c-7c19a7e5f71d'

CORS_ORIGIN_ALLOW_ALL = True
