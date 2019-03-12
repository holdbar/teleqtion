from decimal import Decimal

import redis
from rest_framework import views, permissions, generics, status
from rest_framework.response import Response
from django.conf import settings

from api.v1.permissions import IsOwner
from api.v1.pagination import SmallResultsSetPagination
from .models import Payment
from .utils import create_ipn_hmac
from .exceptions import CoinPaymentsProviderError
from .serializers import PaymentSerializer, CreatePaymentSerializer, \
    CoinPaymentsTransactionSerializer

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)
REDIS_PREFIX = 'RATE:'


class PaymentViewSet(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class CurrenciesView(views.APIView):
    def get(self, request):
        data = list()
        for currency in settings.COINPAYMENTS_ACCEPTED_COINS:
            data.append({
                'symbol': currency[0],
                'name': currency[1],
                'price': round(float(r.get(REDIS_PREFIX + currency[0] + ':USD')), 2)
            })
        return Response(data)


class CreatePaymentView(views.APIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            if serializer.data['amount'] < settings.MIN_PAYMENT_AMOUNT:
                return Response(
                    {'sucess': False,
                     'error': 'Minimum purchase: '
                              '{} USD'.format(settings.MIN_PAYMENT_AMOUNT)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            payment = Payment(
                user=request.user,
                currency_paid=serializer.data['currency'],
                amount=serializer.data['amount'],
                amount_paid=Decimal(0.0),
                status=Payment.PAYMENT_STATUS_PENDING
            )
            try:
                tx = payment.create_tx()
                payment.save()
                return Response(CoinPaymentsTransactionSerializer(tx).data)
            except CoinPaymentsProviderError as e:
                return Response({'success': False, 'error': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class IpnView(views.APIView):

    def post(self, request):
        ipn_mode = request.POST.get('ipn_mode')
        if ipn_mode != 'hmac':
            return Response({'error': 'IPN Mode is not HMAC'},
                            status=status.HTTP_400_BAD_REQUEST)
        http_hmac = request.META.get('HTTP_HMAC')
        if not http_hmac:
            return Response({'error': 'No HMAC signature sent.'},
                            status=status.HTTP_400_BAD_REQUEST)

        our_hmac = create_ipn_hmac(request)
        if our_hmac != http_hmac:
            return Response({'error': 'HMAC mismatch.'},
                            status=status.HTTP_400_BAD_REQUEST)

        merchant_id = getattr(settings, 'COINPAYMENTS_MERCHANT_ID', None)
        if request.POST.get('merchant') != merchant_id:
            return Response({'error': 'Invalid merchant id'},
                            status=status.HTTP_400_BAD_REQUEST)
        tx_id = request.POST.get('txn_id')
        payment = Payment.objects.filter(provider_tx_id__exact=tx_id).first()
        if payment:
            if payment.currency_original != request.POST.get('currency1'):
                return Response({'error': 'Currency mismatch'})
            if payment.status != Payment.PAYMENT_STATUS_PAID:
                payment_status = int(request.POST['status'])
                if payment_status == 2 or payment_status >= 100:
                    payment.amount_paid = Decimal(request.POST['received_amount'])
                elif payment_status == -1:
                    payment.status = Payment.PAYMENT_STATUS_TIMEOUT
                else:
                    payment.amount_paid = Decimal(request.POST['received_amount'])
                if payment.amount_paid >= payment.amount_original:
                    payment.status = Payment.PAYMENT_STATUS_PAID
                    payment.user.update_balance(
                        payment.user.balance + payment.amount
                    )
                payment.save()
