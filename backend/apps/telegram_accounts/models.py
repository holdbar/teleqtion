import uuid
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TelegramAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='telegram_accounts')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(_('Phone Number'), max_length=15)
    phone_code_hash = models.CharField(_('Phone Code Hash'), max_length=20,
                                       blank=True, null=True)
    session = models.CharField(_('Session String'), max_length=500,
                               blank=True, null=True)
    api_id = models.PositiveIntegerField(_('API ID'), blank=True,
                                         default=settings.API_ID)
    api_hash = models.CharField(_('API HASH'), max_length=40, blank=True,
                                default=settings.API_HASH)
    system = models.BooleanField(_('System'), default=False)
    confirmed = models.BooleanField(_('Confirmed'), default=False)
    active = models.BooleanField(_('Active'), default=False,
                                 help_text=_('Banned or not banned.'))
    error_name = models.CharField(_('Error Name'), max_length=15, blank=True, null=True)
    error_datetime = models.DateTimeField(_('Error Datetime'),  blank=True, null=True)
    last_used = models.DateTimeField(_('Last Used'), blank=True, null=True)
    is_used_now = models.BooleanField(_('Is Used Now'), default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Account {}'.format(self.phone_number)

    def deactivate(self, error_name):
        self.error_name = error_name
        self.active = False
        self.error_datetime = timezone.now()
        self.save()

    def update_last_used(self):
        self.last_used = timezone.now()
        self.save()

    @transaction.atomic
    def set_is_used(self, is_used: bool):
        self.is_used_now = is_used
        self.save()

    @property
    def invites_count(self):
        return self.invite_events.count()

    @property
    def messages_count(self):
        return self.message_events.count()
