import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TelegramGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='telegram_groups')

    username = models.CharField(_('Username'), max_length=100,
                                blank=True, null=True, default=None)
    title = models.CharField(_('Title'), max_length=255)
    join_link = models.URLField(_('Join Link'), max_length=255, blank=True,
                                null=True)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Group [{}]'.format(self.title)

    @property
    def scrapped_count(self):
        return self.telegram_contacts.count()

    @property
    def invited_from_count(self):
        return self.invites_from.count()

    @property
    def invited_to_count(self):
        return self.invites_to.count()


class TelegramContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='telegram_contacts')
    group = models.ForeignKey(TelegramGroup,
                              on_delete=models.CASCADE,
                              related_name='telegram_contacts')
    username = models.CharField(_('Username'), max_length=100,
                                blank=True, null=True)
    priority = models.PositiveIntegerField(_('Priority'), blank=True, null=True,
                                           help_text=_('Based on contact activity.'))

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Contact [{}]'.format(self.username)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='messages')
    title = models.CharField(_('Message Title'), max_length=200, blank=True,
                             null=True)
    text = models.TextField(_('Message Text'), max_length=4096)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
