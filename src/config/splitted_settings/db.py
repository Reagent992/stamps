import sys

from config import BASE_DIR
from config.settings import env

USE_POSTGRESQL = env.bool("USE_POSTGRESQL", default=False)

if not USE_POSTGRESQL or "test" in sys.argv:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("DB_NAME", default="PGDB"),
            "USER": env.str("POSTGRES_USER", default="username"),
            "PASSWORD": env.str(
                "POSTGRES_PASSWORD", default="unsafe-password123"
            ),
            "HOST": env.str("DB_HOST", default="db"),
            "PORT": env.int("DB_PORT", default=5432),
        }
    }
