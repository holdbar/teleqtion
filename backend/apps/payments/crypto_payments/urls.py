from django.urls import path
from rest_framework import routers
from . import views

app_name = 'crypto_payments'

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.PaymentViewSet.as_view(), name='payments'),
    path('create', views.CreatePaymentView.as_view(), name='create_payment'),
    path('ipn', views.IpnView.as_view(), name='ipn'),
] + router.urls
