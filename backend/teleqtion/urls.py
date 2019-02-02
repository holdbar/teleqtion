from django.contrib import admin
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
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
