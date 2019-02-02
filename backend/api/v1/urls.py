from rest_framework.routers import DefaultRouter
from django.urls import include, path

from . import views


router = DefaultRouter()

api_urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('telegram-accounts/', include('apps.telegram_accounts.urls')),
    path('task-status/<str:task_id>/', views.GetTaskStatusView.as_view()),
] + router.urls
