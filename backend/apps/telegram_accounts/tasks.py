import random
import time
import logging

from celery.exceptions import SoftTimeLimitExceeded
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import PhoneNumberOccupiedError, SessionPasswordNeededError
import socks

from teleqtion.celery import app as celery_app
from .models import TelegramAccount
from .utils import get_random_user_data, get_new_api_credentials

logger = logging.getLogger(__name__)


@celery_app.task(time_limit=60)
def confirm_account(account_id, code):
    try:
        account = TelegramAccount.objects.get(pk=account_id)

        # for temp account
        proxy_settings_1 = (
            socks.HTTP,
            settings.PROXY_HOST,
            settings.PROXY_PORT, True,
            settings.PROXY_USERNAME+'-session-{}'.format(random.randint(9999, 9999999)),
            settings.PROXY_PASSWORD
        )
        # for new account with own api id and hash
        proxy_settings_2 = (
            socks.HTTP,
            settings.PROXY_HOST,
            settings.PROXY_PORT, True,
            settings.PROXY_USERNAME + '-session-{}'.format(random.randint(9999, 9999999)),
            settings.PROXY_PASSWORD
        )
        client_temp = TelegramClient(StringSession(account.session), account.api_id,
                                     account.api_hash,
                                     proxy=proxy_settings_1)
        client_temp.connect()

        error = None

        try:
            user_data = get_random_user_data()
            client_temp._phone = account.phone_number
            client_temp._phone_code_hash[account.phone_number] = account.phone_code_hash
            client_temp.sign_up(code, user_data['first'], user_data['last'])
        except PhoneNumberOccupiedError:
            client_temp.sign_in(account.phone_number, code,
                                phone_code_hash=account.phone_code_hash)
        except SessionPasswordNeededError:
            error = _('Two Factor Authorization is not yet supported.')
        except Exception as e:
            logger.exception(e)
            error = _('Error during sign in or sign up.')

        if error:
            return {'success': False, 'error': error}

        r = get_new_api_credentials(client_temp, account.phone_number)
        if r.get('error'):
            return {'success': False, 'error': r['error']}

        time.sleep(3)

        try:
            # connecting account with own api id and hash
            client = TelegramClient(StringSession(), r['api_id'], r['api_hash'],
                                    proxy=proxy_settings_2)
            client.connect()
            client.send_code_request(account.phone_number)

            # sleep to allow code arrive
            time.sleep(5)

            # get login code
            messages = client_temp.get_messages(777000, 3)
            code = ''.join([i for i in messages[0].message if i.isdigit()])
            logger.info('code is {}'.format(code))
            client.sign_in(account.phone_number, code)

            myself = client.get_me()

            client_temp.disconnect()
            client.disconnect()

            if myself:
                account.api_id = r['api_id']
                account.api_hash = r['api_hash']
                account.session = client.session.save()
                account.confirmed = True
                account.active = True
                account.last_used = timezone.now()
                account.save()
                return {'success': True, 'error': None}

        except Exception as e:
            logger.exception(e)
            error = _("Error happened. Please, try again later.")
            return {'success': False, 'error': error}
    except SoftTimeLimitExceeded:
        error = _("Error happened. Please, try again later.")
        return {'success': False, 'error': error}
    except Exception as e:
        logger.exception(e)
        error = _("Error happened. Please, try again later.")
        return {'success': False, 'error': error}


@celery_app.task(time_limit=30)
def send_code_request(account_id):
    try:
        account = TelegramAccount.objects.get(pk=account_id)
        try:
            random_confirmed_account = random.choice(
                TelegramAccount.objects.filter(active=True,
                                               confirmed=True)
            )
        except IndexError:
            random_confirmed_account = None
        if random_confirmed_account:
            api_id, api_hash = random_confirmed_account.api_id, random_confirmed_account.api_hash
        else:
            api_id, api_hash = settings.API_ID, settings.API_HASH

        proxy_settings = (
            socks.HTTP,
            settings.PROXY_HOST,
            settings.PROXY_PORT, True,
            settings.PROXY_USERNAME+'-session-{}'.format(random.randint(9999, 9999999)),
            settings.PROXY_PASSWORD
        )

        client = TelegramClient(StringSession(), api_id, api_hash,
                                proxy=proxy_settings)
        client.connect()

        try:
            r = client.send_code_request(account.phone_number,
                                         force_sms=True)
            account.phone_code_hash = r.phone_code_hash
            account.session = client.session.save()
            account.api_id = api_id
            account.api_hash = api_hash
            account.save()
            client.disconnect()

            return {'success': True, 'error': None}
        except Exception as e:
            logger.exception(e)
            return {'success': False, 'error': _('Error sending code request.')}
    except Exception as e:
        logger.exception(e)
        return {'success': False, 'error': _('Error sending code request.')}
