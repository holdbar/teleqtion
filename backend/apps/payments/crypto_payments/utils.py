from django.conf import settings, ImproperlyConfigured

import hmac
import hashlib
from django.utils.http import urlencode


def get_coins_list():
    coins = getattr(settings, 'COINPAYMENTS_ACCEPTED_COINS', None)
    if not coins:
        raise ImproperlyConfigured('COINPAYMENTS_ACCEPTED_COINS setting '
                                   'is required.')
    return coins


def create_ipn_hmac(post_data):
    ipn_secret = getattr(settings, 'COINPAYMENTS_IPN_SECRET', None)
    encoded = urlencode(post_data).encode('utf-8')
    hsh = hmac.new(bytearray(ipn_secret, 'utf-8'), encoded, hashlib.sha512).hexdigest()
    return hsh
