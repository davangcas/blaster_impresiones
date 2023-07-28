from config.settings.base import *
from config.logging import *

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", 'default')
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blaster_impresiones",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "DATABASE_PORT": "5432",
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
