
from pathlib import Path
from environ import Env

env = Env()

# TODO: change env type to .prod when deploying to production
ENVIRONMENT_TYPE = env.str("ENVIRONMENT_TYPE", default=".dev")


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(BASE_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")


APP_DIR = BASE_DIR / "core_apps"


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTH_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist", 
    "drf_yasg",
    "corsheaders",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.users",
    "core_apps.products",
    "core_apps.es_search",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core_apps.products.RateLimiterMiddleware.TokenBucketRateLimitMiddleware", 
]

ROOT_URLCONF = "Img_Twist.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Img_Twist.wsgi.application"

# DB for .dev
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# TODO: change env type to .prod when deploying to production
DATABASES = {"default": env.db("DATABASE_URL")}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

