from dotenv import load_dotenv

from config.settings.base import *
from config.logging import *

load_dotenv(Path.joinpath(BASE_DIR, ".env"))
DEBUG = False
SECRET_KEY = 'django-insecure-nmx2ha(^#qes&%)@a$*36#_5g&od+%_$1h%_vlz*6(4cl1q$9c'
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "DATABASE_PORT": os.environ.get("DB_PORT"),
    }
}
