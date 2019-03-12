import redis
import requests
from django.conf import settings

from teleqtion.celery import app as celery_app


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

REDIS_PREFIX = 'RATE:'


@celery_app.task
def collect_cryptocurrencies_rates():
    try:
        coins_formatted = ','.join(settings.ACCEPTED_COINS_IDS.keys())
        url = 'https://api.coingecko.com/api/v3/' \
              'simple/price?ids={}&vs_currencies=usd'.format(coins_formatted)
        response = requests.get(url).json()
        for currency in response:
            key = REDIS_PREFIX + settings.ACCEPTED_COINS_IDS[currency] + ':USD'
            r.set(key, response[currency]['usd'])

    except Exception as e:
        print(e)
