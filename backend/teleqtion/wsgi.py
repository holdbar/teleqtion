import os
import sys

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from decouple import config


sys.path.append(os.path.join(settings.BASE_DIR, "apps"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      config('DJANGO_SETTINGS_MODULE',
                             default='teleqtion.settings.local'))

application = get_wsgi_application()
