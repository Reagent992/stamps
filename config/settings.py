import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("SECRET_KEY", default="unsafe-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["localhost", "127.0.0.1"])
DATABASES = {
    "default": env.dj_db_url(
        "DATABASE_URL",
        default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3"),
        ssl_require=not DEBUG,
    )
}
# -----------------------------------------------------------------------CELERY
CELERY_BROKER_URL = env.str(
    "CELERY_BROKER_URL",
    default="pyamqp://guest:guest@localhost:5672//",
)
CELERY_RESULT_BACKEND = env.str(
    "CELERY_RESULT_BACKEND",
    default="rpc://guest:guest@localhost:5672//",
)
CELERY_TIMEZONE = "Europe/Moscow"
# ------------------------------------------------------------------------EMAIL
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.yandex.ru")
EMAIL_PORT = env.str("EMAIL_PORT", default="465")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=True)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="email@yandex.ru")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="strong_password")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
if DEBUG:  # output of emailmessage will be in console with debug if true.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Site address. Used in email sending. Must be without "/" at the end.
HOST = env.str("HOST", default="http://localhost:8000")
# Used to receive "new order email".
ADMIN_EMAIL = env.str("ADMIN_EMAIL", default="example@example.com")

# Константа для hostname/sitemap.xml
SITE_ID = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # ---------------------------------Libs------------------------------------
    "sorl.thumbnail",
    "view_breadcrumbs",
    "django_ckeditor_5",
    "debug_toolbar",
    "django_json_widget",
    "crispy_forms",
    "crispy_bootstrap5",
    # ---------------------------------Apps------------------------------------
    "mainapp.apps.MainappConfig",
    "about.apps.AboutConfig",
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
    "debug_toolbar.middleware.DebugToolbarMiddleware",
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

STATIC_URL = "static/"

# -------------------------------------------------------------CUSTOM CONSTANTS
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = BASE_DIR / 'static'
# folder for users images
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PAGINATION_AMOUNT = 4
BREADCRUMBS_HOME_LABEL = "Главная страница"
# ------------------------------------------------------------------------TITLE
END_OF_ALL_TITLES = " - Печати-Архангельск.рф"
INDEX_TITLE = "Главная страница"
ABOUT_CONTACTS_TITLE = "Контакты"
PRINTY_TITLE = "Группы оснасток"
ORDER_TITLE = "Оформление заказа"
ORDER_CREATED = "Заказ оформлен."
# -----------------------------------------------------------------BUTTONS-TEXT
ABOUT_GROUP = "Подробнее о группе"
ABOUT_STAMP = "Подробнее о печати"
ABOUT_PRINTY = "Подробнее о оснастке"
BUTTON_CHOICE_PRINTY = "Выбрать оснастку"
BUTTON_MAKE_ORDER = "Сделать заказ"
BUTTON_WRONG_PRINTY = "Оснастка не подходит под выбранную печать"
# -------------------------------------------------------BREADCRUMBS-HOME-LABEL
PRINTY_LABEL = "Группы оснасток"
# -------------------------------------------------------------BREADCRUMBS-PATH
PRINTY_PATH = "/printy/"
# --------------------------------------------------------------------TEMPLATES
INDEX_TEMPLATE = "mainapp/index.html"
ITEM_DETAIL_TEMPLATE = "mainapp/item_details.html"
ORDER_FORM_TEMPLATE = "mainapp/order_form.html"
ORDER_SUCCESS_TEMPLATE = "mainapp/order_success.html"
# -----------------------------------------------------------------CRISPY-FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# -------------------------------------------------------------------CKEDITOR_5
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css'  # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"  # optional
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    },
}
