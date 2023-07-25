import time

from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "whait for database"

    def handle(self, *args, **options):
        self.stdout.write("waiting for database...")
        db_conn = None

        while not db_conn:
            try:
                database_connection = connection.cursor()
                database_connection.execute("SELECT 1")
                db_conn = True
            except Exception as e:
                self.stdout.write("database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("database available!"))
