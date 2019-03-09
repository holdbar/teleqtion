from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from api.v1.urls import api_urlpatterns as api_v1

# admin settings
admin.site.site_header = _('Teleqtion Administration')
admin.site.site_title = _('Teleqtion Administration')
admin.site.index_title = _('Teleqtion')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1)),
    path('login/', TemplateView.as_view(template_name='login.html'),
         name='login'),
    path('signup/', TemplateView.as_view(template_name='signup.html'),
         name='signup'),
    path('confirm-account/<str:key>/',
         TemplateView.as_view(template_name='confirm-account.html'),
         name='confirm_account'),
    path('reset-password/',
         TemplateView.as_view(template_name='reset-password.html'),
         name='password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/',
         TemplateView.as_view(template_name='reset-password-confirm.html'),
         name='password_reset_confirm'),
    path('email-sent/', TemplateView.as_view(template_name='email-sent.html'),
         name='account_email_verification_sent'),
    path('', TemplateView.as_view(template_name='index.html'),
         name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
