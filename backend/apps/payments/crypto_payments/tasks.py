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
        coins_formatted = ','.join([i[0] for i in settings.COINPAYMENTS_ACCEPTED_COINS])
        url = 'https://pro-api.coinmarketcap.com/' \
              'v1/cryptocurrency/quotes/latest' \
              '?symbol={}&convert=USD'.format(coins_formatted)
        headers = {'X-CMC_PRO_API_KEY': settings.COINMARKETCAP_API_KEY}
        response = requests.get(url, headers=headers).json()
        if response['status']['error_code'] != 0:
            return

        for currency in response['data']:
            key = REDIS_PREFIX + currency + ':USD'
            r.set(key, response['data'][currency]['quote']['USD']['price'])

    except Exception as e:
        print(e)
