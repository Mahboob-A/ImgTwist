
from .base import * # noqa 
from .base import env  # noqa



# ################# Security 

SECRET_KEY = "django-insecure-bjp)78vk8e0hddyl+ot4+b=x*s63_pt7j&3vb$bplzxa!4t0r="

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",  # Django Developement Server
    "http://127.0.0.1:8080",  # Dockerizedd Django App with Nginx
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Django Developement Server
    "http://127.0.0.1:8080",  # Dockerizedd Django App with Nginx
]


############################ ADDED SETTINGS ###############################

# ################# Static and Media

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")


ADMIN_URL = env("ADMIN_URL")


# ################# DRF Settings 
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}



# ################# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    
    # db query logs 
    # "loggers": {
    #     "django.db": {
    #         "level": "DEBUG",
    #         "handlers": ["console"],
    #     }
    # },
}