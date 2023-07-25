from dotenv import load_dotenv

from config.settings.base import *
from config.logging import *

load_dotenv(Path.joinpath(BASE_DIR, ".env"))
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "default")
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
