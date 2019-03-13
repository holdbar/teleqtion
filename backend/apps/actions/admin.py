from django.contrib import admin

from .models import InviteEvent, MessageEvent


admin.site.register(InviteEvent)
admin.site.register(MessageEvent)
