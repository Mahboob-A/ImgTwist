"""
ASGI config for Img_Twist project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# TODO: change env type to .prod when deploying to production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Img_Twist.settings.dev")

application = get_asgi_application()
