"""Nautobot development configuration file."""
import os
import sys

from nautobot.core.settings import *
from nautobot.core.settings_funcs import is_truthy

ALLOWED_HOSTS = os.environ.get("NAUTOBOT_ALLOWED_HOSTS", "").split(" ")

DATABASES = {
    "default": {
        "NAME": os.environ.get("NAUTOBOT_DB_NAME", "nautobot"),
        "USER": os.environ.get("NAUTOBOT_DB_USER", ""),
        "PASSWORD": os.environ.get("NAUTOBOT_DB_PASSWORD", ""),
        "HOST": os.environ.get("NAUTOBOT_DB_HOST", "localhost"),
        "PORT": os.environ.get("NAUTOBOT_DB_PORT", ""),
        "CONN_MAX_AGE": 300,
        "ENGINE": "django.db.backends.postgresql",
    }
}

DEBUG = True

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# Verbose logging during normal development operation, but quiet logging during unit test execution
if not TESTING:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "normal": {
                "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)s :\n  %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "verbose": {
                "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-20s %(filename)-15s %(funcName)30s() :\n  %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "normal_console": {
                "level": "INFO",
                "class": "rq.utils.ColorizingStreamHandler",
                "formatter": "normal",
            },
            "verbose_console": {
                "level": "DEBUG",
                "class": "rq.utils.ColorizingStreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {"handlers": ["normal_console"], "level": "INFO"},
            "nautobot": {
                "handlers": ["verbose_console" if DEBUG else "normal_console"],
                "level": LOG_LEVEL,
            },
            "nautobot_data_validation_engine": {
                "handlers": ["verbose_console" if DEBUG else "normal_console"],
                "level": LOG_LEVEL,
            },
            "rq.worker": {
                "handlers": ["verbose_console" if DEBUG else "normal_console"],
                "level": LOG_LEVEL,
            },
        },
    }


# Redis variables
REDIS_HOST = os.getenv("NAUTOBOT_REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("NAUTOBOT_REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("NAUTOBOT_REDIS_PASSWORD", "")

# Check for Redis SSL
REDIS_SCHEME = "redis"
REDIS_SSL = is_truthy(os.environ.get("NAUTOBOT_REDIS_SSL", False))
if REDIS_SSL:
    REDIS_SCHEME = "rediss"

# The django-redis cache is used to establish concurrent locks using Redis. The
# django-rq settings will use the same instance/database by default.
#
# This "default" server is now used by RQ_QUEUES.
# >> See: nautobot.core.settings.RQ_QUEUES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_SCHEME}://{REDIS_HOST}:{REDIS_PORT}/0",
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        },
    }
}

# RQ_QUEUES is not set here because it just uses the default that gets imported
# up top via `from nautobot.core.settings import *`.

# REDIS CACHEOPS
CACHEOPS_REDIS = f"{REDIS_SCHEME}://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1"

HIDE_RESTRICTED_UI = os.environ.get("HIDE_RESTRICTED_UI", False)

SECRET_KEY = os.environ.get("NAUTOBOT_SECRET_KEY", "")

# Django Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG and not TESTING}

if "debug_toolbar" not in INSTALLED_APPS:
    INSTALLED_APPS.append("debug_toolbar")
if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = ["nautobot_data_validation_engine"]
