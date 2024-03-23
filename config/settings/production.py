from dotenv import load_dotenv

from config.logging import *
from config.settings.base import *

load_dotenv(Path.joinpath(BASE_DIR, ".env"))
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "default")
ALLOWED_HOSTS = [
    "www.blasterimpresiones.com",
    "blasterimpresiones.com",
]

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

STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
