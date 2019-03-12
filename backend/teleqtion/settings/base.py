import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',

    'apps.users',
    'apps.telegram_accounts',
    'apps.actions',
    'apps.telegram_entities',
    'apps.payments.crypto_payments',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'teleqtion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'teleqtion.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static/')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')
FILE_UPLOAD_MAX_MEMORY_SIZE = 5324800

AUTH_USER_MODEL = 'users.User'

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 360
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_DISPLAY = 'users.utils.get_user_display'
ACCOUNT_ADAPTER = 'users.adapters.CustomAccountAdapter'

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'apps.users.serializers.CustomLoginSerializer',
    'USER_DETAILS_SERIALIZER': 'apps.users.serializers.CustomUserDetailsSerializer',
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'apps.users.serializers.CustomRegisterSerializer',
}
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}
# APPEND_SLASH = False

# Prices
PRICE_USING_OWN_NUMBERS = 0.04
PRICE_USING_SYSTEM_NUMBERS = 0.06
MIN_PAYMENT_AMOUNT = 5.0

COINPAYMENTS_ACCEPTED_COINS = (
    ('BTC', 'Bitcoin'),
    ('LTC', 'Litecoin'),
    ('BCH', 'Bitcoin Cash'),
    ('DASH', 'Dash'),
    ('ETH', 'Ether'),
    ('QTUM', 'Qtum'),
    ('TUSD', 'TrueUSD'),
    ('WAVES', 'Waves'),
)

# for prices caching from CoinGecko
ACCEPTED_COINS_IDS = {
    'bitcoin': 'BTC',
    'litecoin': 'LTC',
    'bitcoin-cash': 'BCH',
    'dash': 'DASH',
    'ethereum': 'ETH',
    'qtum': 'QTUM',
    'true-usd': 'TUSD',
    'waves': 'WAVES'
}
