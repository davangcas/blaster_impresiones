import ast
import os
from pathlib import Path

from dotenv import load_dotenv

from config.logging import *  # noqa: F403
from config.settings.base import *  # noqa: F403
from config.settings.base import BASE_DIR

load_dotenv(Path.joinpath(BASE_DIR, ".env"))
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "default")
ALLOWED_HOSTS = ast.literal_eval(os.environ.get("ALLOWED_HOSTS", "['*']"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Static files (CSS, JavaScript, images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = Path.joinpath(BASE_DIR, "staticfiles")
