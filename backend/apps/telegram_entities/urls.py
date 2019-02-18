from rest_framework import routers
from . import views

app_name = 'telegram_entities'

router = routers.DefaultRouter()
router.register(r'groups', views.TelegramGroupViewSet,
                base_name='telegram_group')
router.register(r'contacts', views.TelegramContactViewSet,
                base_name='telegram_contact')
router.register(r'messages', views.MessageViewSet, base_name='message')

urlpatterns = [] + router.urls
