from django.conf import settings

POSTGRES_LOCAL_DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blaster_impresiones",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "DATABASE_PORT": "5432",
    }
}

POSTGRES_PRODUCTION_DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "blaster_impresiones",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "DATABASE_PORT": "5432",
    }
}
