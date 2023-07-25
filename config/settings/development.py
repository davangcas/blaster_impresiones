from config.settings.base import *
from config.logging import *

DEBUG = True
SECRET_KEY = 'django-insecure-nmx2ha(^#qes&%)@a$*36#_5g&od+%_$1h%_vlz*6(4cl1q$9c'
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
