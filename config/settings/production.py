import ast

from dotenv import load_dotenv

from config.logging import *
from config.settings.base import *

load_dotenv(Path.joinpath(BASE_DIR, ".env"))
DEBUG = ast.literal_eval(os.environ.get("DEBUG", "False"))
SECRET_KEY = os.environ.get("SECRET_KEY", "default")
ALLOWED_HOSTS = [
    "https://www.blasterimpresiones.com",
    "https://blasterimpresiones.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "DATABASE_PORT": os.environ.get("DB_PORT"),
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
