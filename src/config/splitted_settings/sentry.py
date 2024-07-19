import sentry_sdk

from config.settings import env

sentry_sdk.init(
    dsn=env.str("DSN", default=""),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=env.float("TRACES", default=1.0),
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=env.float("PROFILES", default=1.0),
)
