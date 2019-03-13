from django.contrib import admin

from .models import TelegramContact, TelegramGroup, Message

admin.site.register(TelegramContact)
admin.site.register(TelegramGroup)
admin.site.register(Message)
