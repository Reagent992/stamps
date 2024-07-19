from config.settings import env

CELERY_BROKER_URL = env.str(
    "CELERY_BROKER_URL",
    default="pyamqp://guest:guest@localhost:5672//",
)
CELERY_RESULT_BACKEND = env.str(
    "CELERY_RESULT_BACKEND",
    default="rpc://guest:guest@localhost:5672//",
)
CELERY_TIMEZONE = "Europe/Moscow"

TASK_BEGIN_DELAY = 1
