"""
WSGI config for Img_Twist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# TODO: change env type to .prod when deploying to production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Img_Twist.settings.dev")

application = get_wsgi_application()
