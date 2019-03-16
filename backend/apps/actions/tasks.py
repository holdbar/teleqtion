import random
import logging

from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsRecent
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import PeerFloodError, \
    UserDeactivatedError, AuthKeyUnregisteredError, ChannelsTooMuchError, \
    ChannelPrivateError, ChatAdminRequiredError, ChatWriteForbiddenError, \
    InputUserDeactivatedError, UsersTooMuchError, UserBannedInChannelError, \
    ChatInvalidError, ChatIdInvalidError
import socks

from teleqtion.celery import app as celery_app
from apps.telegram_accounts.models import TelegramAccount
from apps.telegram_entities.models import TelegramGroup, TelegramContact, Message
from apps.actions.models import InviteEvent, MessageEvent

from .utils import join_group

User = get_user_model()
logger = logging.getLogger(__name__)


@celery_app.task(time_limit=120)
def invites_task(limit, user_id, source_group_id, target_group_id,
                 numbers_list=None, use_system_numbers=False):
    user = User.objects.get(pk=user_id)
    source_group = TelegramGroup.objects.get(pk=source_group_id)
    target_group = TelegramGroup.objects.get(pk=target_group_id)

    if use_system_numbers:
        price = settings.PRICE_USING_SYSTEM_NUMBERS
        active_accounts = TelegramAccount.objects.filter(system=True,
                                                         confirmed=True,
                                                         active=True,
                                                         is_used_now=False)
    else:
        price = settings.PRICE_USING_OWN_NUMBERS
        # active_accounts = TelegramAccount.objects.filter(id__in=numbers_list,
        #                                                  user=user,
        #                                                  system=False,
        #                                                  confirmed=True,
        #                                                  active=True,
        #                                                  is_used_now=False)
        active_accounts = TelegramAccount.objects.filter(user=user,
                                                         system=False,
                                                         confirmed=True,
                                                         active=True,
                                                         is_used_now=False)
    if not active_accounts:
        return {'success': False, 'error': _('No active accounts left.')}

    invited = 0
    try:
        for account in active_accounts:
            # mark being used now, so account won't be used in other tasks
            account.set_is_used(True)

            proxy_settings = (
                socks.HTTP,
                settings.PROXY_HOST,
                settings.PROXY_PORT, True,
                settings.PROXY_USERNAME + '-session-{}'.format(random.randint(9999,
                                                                              9999999)),
                settings.PROXY_PASSWORD
            )
            client = TelegramClient(StringSession(account.session),
                                    account.api_id, account.api_hash,
                                    proxy=proxy_settings)
            # connect to Telegram
            try:
                client.connect()
            except Exception as e:
                logger.exception(e)
                account.set_is_used(False)
                continue

            # get target group entity
            try:
                target_group_entity = client.get_input_entity(
                    target_group.username if target_group.username
                    else target_group.join_link
                )
            except Exception as e:
                logger.exception(e)
                client.disconnect()
                account.set_is_used(False)
                return {'success': False, 'error': _('Target Group invalid.')}

            # join channel
            joined = join_group(client, account, target_group)
            if not joined:
                account.set_is_used(False)
                client.disconnect()
                continue
            elif isinstance(joined, dict):  # means there was an error
                client.disconnect()
                return joined

            # find not invited contacts or with errors
            invites = InviteEvent.objects.filter(
                Q(success=True) | Q(error__isnull=False),
                user=user,
                source_group=source_group,
                target_group=target_group
            )
            processed_contacts = [i.contact for i in invites]
            contacts = [c for c in
                        TelegramContact.objects.filter(user=user, group=source_group)
                            .order_by('priority')
                        if c not in processed_contacts]

            # invite contacts
            for contact in contacts:
                if invited >= limit:
                    account.set_is_used(False)
                    client.disconnect()
                    return {'success': True, 'error': None}
                if user.balance <= 0:
                    account.set_is_used(False)
                    client.disconnect()
                    return {'success': False, 'error': _('Not enough funds. Please, '
                                                         'refill your balance.')}
                try:
                    client(InviteToChannelRequest(
                        target_group_entity,
                        [contact.username]
                    ))
                    invited += 1
                    user.update_balance(-price)
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               contact=contact,
                                               success=True,
                                               price=price)

                # errors with account
                except (PeerFloodError, AuthKeyUnregisteredError, UserDeactivatedError,
                        ChatWriteForbiddenError, UserBannedInChannelError,
                        ChannelsTooMuchError) as e:
                    logger.exception(e)
                    account.deactivate(e.__class__.__name__)
                    account.set_is_used(False)
                    client.disconnect()
                    break

                # critical errors, when we need to stop inviting
                except ChannelPrivateError as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               error=e.__class__.__name__)
                    account.update_last_used()
                    account.set_is_used(False)
                    client.disconnect()
                    return {'success': False, 'error': _('Cannot invite to Channel, '
                                                         'since it is private.')}
                except (ChatInvalidError, ChatIdInvalidError) as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               error=e.__class__.__name__)
                    account.update_last_used()
                    account.set_is_used(False)
                    client.disconnect()
                    return {'success': False, 'error': _('Cannot invite to Channel, '
                                                         'since it is private.')}
                except ChatAdminRequiredError as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               error=e.__class__.__name__)
                    account.update_last_used()
                    account.set_is_used(False)
                    client.disconnect()
                    return {'success': False, 'error': _('Cannot invite to Channel, '
                                                         'since it admin rights are required.')}

                except InputUserDeactivatedError as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               contact=contact,
                                               error=e.__class__.__name__)
                    account.update_last_used()
                except UsersTooMuchError as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               error=e.__class__.__name__)
                    account.update_last_used()
                    client.disconnect()
                    return {'success': False, 'error': _('Cannot invite to Channel, '
                                                         'since it has already reached the '
                                                         'maximum number of users.')}
                # other errors
                except Exception as e:
                    InviteEvent.objects.create(user=user,
                                               source_group=source_group,
                                               target_group=target_group,
                                               telegram_account=account,
                                               contact=contact,
                                               error=e.__class__.__name__)
                    account.update_last_used()

            account.set_is_used(False)

            if client.is_connected():
                client.disconnect()

        return {'success': True, 'error': None}
    except Exception as e:
        logger.exception(e)
        return {'success': True, 'error': None}


@celery_app.task(time_limit=120)
def scrape_task(user_id, group_id, tg_account_id=None):
    user = User.objects.get(pk=user_id)
    group = TelegramGroup.objects.get(pk=group_id)
    if tg_account_id:
        account = TelegramAccount.objects.get(pk=tg_account_id)
    else:
        try:
            account = random.choice(
                TelegramAccount.objects.filter(active=True,
                                               confirmed=True)
            )
        except IndexError:
            return {'success': False, 'error': _('No available active accounts '
                                                 'for scrapping.')}
    proxy_settings = (
        socks.HTTP,
        settings.PROXY_HOST,
        settings.PROXY_PORT, True,
        settings.PROXY_USERNAME + '-session-{}'.format(random.randint(9999, 9999999)),
        settings.PROXY_PASSWORD
    )
    account.set_is_used(True)
    client = TelegramClient(StringSession(account.session), account.api_id,
                            account.api_hash, proxy=proxy_settings)
    client.connect()

    try:
        try:
            group_entity = client.get_input_entity(group.username if group.username
                                                   else group.join_link)
        except Exception as e:
            logger.exception(e)
            account.set_is_used(False)
            client.disconnect()
            return {'success': False, 'error': _('Error finding group.')}

        joined = join_group(client, account, group_entity)
        if not joined:
            account.set_is_used(False)
            client.disconnect()
            return {'success': False, 'error': _('Error joining group.')}
        elif isinstance(joined, dict):  # means there was an error
            account.set_is_used(False)
            client.disconnect()
            return joined

        try:
            members = client.get_participants(group_entity, aggressive=True,
                                              filter=ChannelParticipantsRecent())
            admins = client.get_participants(group_entity, aggressive=True,
                                             filter=ChannelParticipantsAdmins())
            members = [m for m in members if not m.bot and  # skip bots
                       m not in admins and  # skip admins
                       m.username and  # skip without usernames
                       not m.is_self]  # skip if members is current client user
        except:
            account.set_is_used(False)
            client.disconnect()
            return {'success': False, 'error': _('Error getting list of group '
                                                 'members.')}
        client.disconnect()
        account.set_is_used(False)
        with transaction.atomic():
            for i, m in enumerate(members):
                TelegramContact.objects.get_or_create(user=user,
                                                      group=group,
                                                      username=m.username,
                                                      priority=i + 1)
        message = _('Scrapped {} users.'.format(len(members)))
        return {'success': True, 'error': None, 'message': message}
    except Exception as e:
        logger.exception(e)
        return {'success': True, 'error': _('Error getting list of group '
                                            'members.')}


@celery_app.task(time_limit=120)
def messages_task(limit, user_id, group_id, message_id,
                  numbers_list=None, use_system_numbers=False):
    user = User.objects.get(pk=user_id)
    group = TelegramGroup.objects.get(pk=group_id)
    message = Message.objects.get(pk=message_id)

    if use_system_numbers:
        price = settings.PRICE_USING_SYSTEM_NUMBERS
        active_accounts = TelegramAccount.objects.filter(system=True,
                                                         confirmed=True,
                                                         active=True,
                                                         is_used_now=False)
    else:
        price = settings.PRICE_USING_OWN_NUMBERS
        # active_accounts = TelegramAccount.objects.filter(id__in=numbers_list,
        #                                                  user=user,
        #                                                  system=False,
        #                                                  confirmed=True,
        #                                                  active=True,
        #                                                  is_used_now=False)
        active_accounts = TelegramAccount.objects.filter(user=user,
                                                         system=False,
                                                         confirmed=True,
                                                         active=True,
                                                         is_used_now=False)
    if not active_accounts:
        return {'success': False, 'error': _('No active accounts left.')}

    messaged = 0

    try:
        for account in active_accounts:
            # mark being used now, so account won't be used in other tasks
            account.set_is_used(True)

            proxy_settings = (
                socks.HTTP,
                settings.PROXY_HOST,
                settings.PROXY_PORT, True,
                settings.PROXY_USERNAME + '-session-{}'.format(random.randint(9999,
                                                                              9999999)),
                settings.PROXY_PASSWORD
            )
            client = TelegramClient(StringSession(account.session),
                                    account.api_id, account.api_hash,
                                    proxy=proxy_settings)
            # connect to Telegram
            try:
                client.connect()
            except Exception as e:
                logger.exception(e)
                account.set_is_used(False)
                continue

            # find not messaged contacts or with errors
            message_events = MessageEvent.objects.filter(
                Q(success=True) | Q(error__isnull=False),
                user=user,
                telegram_group=group,
                message=message
            )
            processed_contacts = [i.contact for i in message_events]
            contacts = [c for c in
                        TelegramContact.objects.filter(user=user, group=group)
                            .order_by('priority')
                        if c not in processed_contacts]

            # send messages to contacts
            for contact in contacts:
                if messaged >= limit:
                    client.disconnect()
                    account.set_is_used(False)
                    return {'success': True, 'error': None}
                if user.balance <= 0:
                    client.disconnect()
                    account.set_is_used(False)
                    return {'success': False, 'error': _('Not enough funds. Please, '
                                                         'refill your balance.')}
                try:
                    if message.file:
                        client.send_message(contact.username, message.text,
                                            file=message.file.path,
                                            link_preview=message.link_preview,
                                            parse_mode='html')
                    else:
                        client.send_message(contact.username, message.text,
                                            link_preview=message.link_preview,
                                            parse_mode='html')
                    messaged += 1
                    user.update_balance(-price)
                    MessageEvent.objects.create(user=user,
                                                telegram_group=group,
                                                telegram_account=account,
                                                contact=contact,
                                                success=True,
                                                message=message,
                                                price=price)

                # errors with account
                except (PeerFloodError, AuthKeyUnregisteredError, UserDeactivatedError,
                        ChatWriteForbiddenError, UserBannedInChannelError,
                        ChannelsTooMuchError) as e:
                    client.disconnect()
                    account.set_is_used(False)
                    account.deactivate(e.__class__.__name__)
                    break
                except Exception as e:
                    MessageEvent.objects.create(user=user,
                                                telegram_group=group,
                                                contact=contact,
                                                telegram_account=account,
                                                message=message,
                                                error=e.__class__.__name__)
                    account.update_last_used()

            account.set_is_used(False)

            if client.is_connected():
                client.disconnect()

        return {'success': True, 'error': None}
    except Exception as e:
        logger.exception(e)
        return {'success': True, 'error': _('Error sending message.')}
