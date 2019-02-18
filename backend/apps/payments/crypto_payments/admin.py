from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Payment, CoinPaymentsTransaction


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency_original', 'currency_paid',
                    'amount', 'status')
    list_filter = ('status',)


class CoinPaymentsTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'amount', 'link_to_payment')

    def link_to_payment(self, obj):
        if hasattr(obj, 'payment'):
            link = reverse("admin:crypto_payments_payment_change",
                           args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', link, obj.payment.id)
        return '-'

    link_to_payment.short_description = _('Payment')


admin.site.register(Payment, PaymentAdmin)
admin.site.register(CoinPaymentsTransaction, CoinPaymentsTransactionAdmin)
