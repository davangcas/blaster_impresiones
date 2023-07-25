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
        "HOST": "postgres",
        "DATABASE_PORT": "5432",
    }
}
