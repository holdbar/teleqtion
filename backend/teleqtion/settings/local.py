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
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/3'
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/3'

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
