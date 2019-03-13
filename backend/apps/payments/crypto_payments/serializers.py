from rest_framework import serializers

from .models import Payment, CoinPaymentsTransaction
from .utils import get_coins_list


class CreatePaymentSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    amount = serializers.DecimalField(decimal_places=18, max_digits=65,
                                      coerce_to_string=False)
    currency = serializers.ChoiceField(get_coins_list())


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    currency = serializers.CharField(source='currency_paid')
    amount = serializers.DecimalField(decimal_places=18, max_digits=65,
                                      coerce_to_string=False)
    amount_paid = serializers.DecimalField(decimal_places=18, max_digits=65,
                                           coerce_to_string=False)
    amount_original = serializers.DecimalField(decimal_places=18, max_digits=65,
                                               coerce_to_string=False)

    class Meta:
        model = Payment
        fields = ('user', 'currency', 'amount',
                  'amount_paid', 'amount_original', 'status', 'created_at')


class CoinPaymentsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPaymentsTransaction
        fields = '__all__'
