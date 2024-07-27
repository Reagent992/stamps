from environs import Env

env = Env()
env.read_env()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME", default="stamps"),
        "USER": env.str("POSTGRES_USER", default="username"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="unsafe-password123"),
        "HOST": env.str("DB_HOST", default="db"),
        "PORT": env.int("DB_PORT", default=5432),
    }
}
