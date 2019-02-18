from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.telegram_accounts.models import TelegramAccount
from apps.telegram_entities.models import TelegramGroup, TelegramContact, Message


class InviteEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='invite_events')
    telegram_account = models.ForeignKey(
        TelegramAccount,
        on_delete=models.CASCADE,
        related_name='invite_events'
    )
    source_group = models.ForeignKey(TelegramGroup,
                                     on_delete=models.CASCADE,
                                     related_name='invites_from')
    target_group = models.ForeignKey(TelegramGroup,
                                     on_delete=models.CASCADE,
                                     related_name='invites_to')
    contact = models.ForeignKey(TelegramContact,
                                on_delete=models.CASCADE,
                                related_name='invites',
                                blank=True, null=True)
    success = models.BooleanField(_('Success'), default=False)
    price = models.FloatField(_('Price'), default=0)
    error = models.CharField(_('Error'), max_length=100, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)


class MessageEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='message_events')
    telegram_account = models.ForeignKey(
        TelegramAccount,
        on_delete=models.CASCADE,
        related_name='message_events'
    )
    telegram_group = models.ForeignKey(TelegramGroup,
                                       on_delete=models.CASCADE,
                                       related_name='message_events')
    contact = models.ForeignKey(TelegramContact,
                                on_delete=models.CASCADE,
                                related_name='message_events',
                                blank=True, null=True)
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                related_name='message_events')
    success = models.BooleanField(_('Success'), default=False)
    error = models.CharField(_('Error'), max_length=100, blank=True, null=True)
    price = models.FloatField(_('Price'), default=0)
    datetime = models.DateTimeField(auto_now_add=True)
