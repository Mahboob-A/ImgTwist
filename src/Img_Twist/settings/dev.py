from datetime import timedelta

from .base import *  # noqa
from .base import env  # noqa

# ################# Security

SECRET_KEY = env.str("SECRET_KEY")
DJANGO_APP_PORT = env("DJANGO_APP_PORT")


DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "imgtwist.algocode.site"]

# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:8000",  # Django Developement Server
#     "http://127.0.0.1:8080",  # Dockerizedd Django App with Nginx
# ]

# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000",  # Django Developement Server
#     "http://127.0.0.1:8080",  # Dockerizedd Django App with Nginx
# ]


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "https://imgtwist.algocode.site",
    "https://algocode.site",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "https://imgtwist.algocode.site",
    "https://algocode.site",
]


############################ ADDED SETTINGS ###############################

# ################# Static and Media

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "mediafiles")


ADMIN_URL = env("ADMIN_URL")


# ################# Local Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 300,
        "OPTIONS": {
            "MAX_ENTRIES": 1000,
        },
    }
}


# ##################### DRF Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/minute",
        "user": "10/minute",
    },
}

# ##################### JWT Settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SIGNING_KEY": env("JWT_SIGNING_KEY"),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "id",
    "USER_IF_CLAIM": "user_id",
}

# ##################### Auth Backends
AUTHENTICATION_BACKENDS = [
    "core_apps.users.auth_backend.EmailAndUsernameCredentialAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ##################### Auth User Model
AUTH_USER_MODEL = "users.CustomUser"


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
