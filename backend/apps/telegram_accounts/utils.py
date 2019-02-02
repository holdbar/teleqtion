import random
import time

import requests
from lxml import etree


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/72.0.3626.81 Safari/537.36'

default_data = [
    {'first': 'Lonne', 'last': 'Loer', 'avatar': None},
    {'first': 'Frank', 'last': 'Hicks', 'avatar': None},
    {'first': 'Ciro', 'last': 'Poell', 'avatar': None},
    {'first': 'Tracy', 'last': 'Vargas', 'avatar': None},
    {'first': 'Corey', 'last': 'Peterson', 'avatar': None},
    {'first': 'Lylou', 'last': 'Gautier', 'avatar': None},
    {'first': 'Denise', 'last': 'Ruiz', 'avatar': None},
    {'first': 'Oscar', 'last': 'Sims', 'avatar': None},
    {'first': 'Marceau', 'last': 'Berhard', 'avatar': None},
    {'first': 'Sebastian', 'last': 'Kumar', 'avatar': None},
]


def get_random_user_data():
    url = 'https://randomuser.me/api/?nat=au,ca,fr,gb,ie,nl,nz,us' \
          '&inc=name,picture&noinfo'
    try:
        r = requests.get(url).json()
        return {
                   'first': r['results'][0]['name']['first'].capitalize(),
                   'last': r['results'][0]['name']['last'].capitalize(),
                   'avatar': r['results'][0]['picture']['large']
        }
    except:
        return random.choice(default_data)


def get_new_api_credentials(client, phone_number):
    try:
        s = requests.Session()
        s.headers.update({'User-Agent': user_agent, 'Connection': 'close'})

        # get cookies
        s.get('https://my.telegram.org/auth')

        # send request
        r = s.post('https://my.telegram.org/auth/send_password',
                   data={'phone': phone_number}).json()
        random_hash = r.get('random_hash')
        if not random_hash:
            error = 'Error getting code from my.telegram.org'
            return {'error': error}

        time.sleep(5)

        # get code from telegram
        messages = client.get_messages(777000, 3)
        code = messages[0].message.split('\n')[1]

        # login to my.telegram.org
        s.post('https://my.telegram.org/auth/login',
               data={'phone': phone_number,
                     'random_hash': random_hash,
                     'password': code})

        # create app
        r = s.get('https://my.telegram.org/apps')
        if not etree.HTML(r.text).xpath('//*[@id="app_edit_form"]/div[1]/div[1]/span/strong'):
            hidden_hash = str(etree.HTML(r.text).xpath('//input[@name="hash"]/@value')[0])
            s.post('https://my.telegram.org/apps/create',
                   data={'hash': hidden_hash,
                         'app_title': 'MyTgApp',
                         'app_shortname': 'MyTgApp',
                         'app_url': 'mysite.com',
                         'app_platform': 'android',
                         'app_desc': 'automated app'
                         })
        r = s.get('https://my.telegram.org/apps')
        api_id = int(etree.HTML(r.text).xpath('//strong')[0].text)
        api_hash = etree.HTML(r.text).xpath('//span[@class="form-control '
                                            'input-xlarge uneditable-input"]')[1].text

        return {'api_id': api_id, 'api_hash': api_hash}

    except:
        return {'error': 'Sign in / Sign up failed.'}
