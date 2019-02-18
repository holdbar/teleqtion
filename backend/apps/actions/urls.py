from rest_framework import routers
from django.urls import path
from . import views

app_name = 'actions'

router = routers.DefaultRouter()

urlpatterns = [
    path('scrapping/start', views.StartScrappingView.as_view(),
         name='start_scrapping'),
    path('inviting/start', views.StartInvitingView.as_view(),
         name='start_inviting'),
    path('messaging/start', views.StartMessagingView.as_view(),
         name='start_messaging'),
] + router.urls
