import sys
from pathlib import Path

from environs import Env
from split_settings.tools import include

env = Env()
env.read_env()
# Most settings moved to splitted_settings folder.
include(
    "splitted_settings/*"
)
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("SECRET_KEY", default="unsafe-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://localhost", "http://127.0.0.1"]
)
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    # ---------------------------------Libs------------------------------------
    "sorl.thumbnail",
    "view_breadcrumbs",
    "django_ckeditor_5",
    "django_json_widget",
    "crispy_forms",
    "crispy_bootstrap5",
    # ---------------------------------Apps------------------------------------
    "mainapp.apps.MainappConfig",
    "printy.apps.PrintyConfig",
    "core.apps.CoreConfig",
    "orders.apps.OrdersConfig",
    "stamp_fields.apps.StampFieldsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.year.year",
                "core.context_processors.title.title",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


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

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = False

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

STATICFILES_DIRS = ((BASE_DIR / "static"),)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collected_static"
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR / "media")
# ---------------------------------------------------------DJANGO DEBUG TOOLBAR
TESTING = "test" in sys.argv

if not TESTING and DEBUG is True:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]
    # this code allow use debug_toolbar in docker
    import socket

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
