from rest_framework import routers
from . import views

app_name = 'telegram_accounts'

router = routers.DefaultRouter()
router.register(r'', views.TelegramAccountViewSet, base_name='telegram_account')

urlpatterns = [] + router.urls
