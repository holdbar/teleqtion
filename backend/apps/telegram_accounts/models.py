from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TelegramAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='telegram_accounts')

    phone_number = models.CharField(_('Phone Number'), max_length=15)
    phone_code_hash = models.CharField(_('Phone Code Hash'), max_length=20,
                                       blank=True, null=True)
    session = models.CharField(_('Session String'), max_length=500,
                               blank=True, null=True)
    api_id = models.PositiveIntegerField(_('API ID'), blank=True, null=True)
    api_hash = models.CharField(_('API HASH'), max_length=30, blank=True, null=True)
    system = models.BooleanField(_('System'), default=False)
    confirmed = models.BooleanField(_('Confirmed'), default=False)
    active = models.BooleanField(_('Active'), default=True,
                                 help_text=_('Banned or not banned.'))
    error_name = models.CharField(_('Error Name'), max_length=15, blank=True, null=True)
    error_datetime = models.DateTimeField(_('Error Datetime'),  blank=True, null=True)

    last_used = models.DateTimeField(_('Last Used'), blank=True, null=True)
    messages_count = models.PositiveIntegerField(_('Sent Messages'),
                                                 blank=True, null=True)
    invites_count = models.PositiveIntegerField(_('Successful Invites'),
                                                blank=True, null=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Account {}'.format(self.phone_number)
