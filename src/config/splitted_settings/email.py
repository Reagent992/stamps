from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", default=False)

EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.yandex.ru")
EMAIL_PORT = env.str("EMAIL_PORT", default="465")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=True)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="email@yandex.ru")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="strong_password")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Output of emailmessage will be in console with debug if true.
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Site address. Used in email sending. Must be without "/" at the end.
HOST = env.str("HOST", default="http://localhost:8000")
# Used to receive "new order email".
ADMIN_EMAIL = env.str("ADMIN_EMAIL", default="example@example.com")
