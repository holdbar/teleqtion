from django.contrib import admin

from .models import TelegramAccount


class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'system', 'confirmed',
                    'active', 'added_at')


admin.site.register(TelegramAccount, TelegramAccountAdmin)
