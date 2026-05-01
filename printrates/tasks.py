from celery import shared_task

from prints.models import Print


@shared_task
def refresh_prints_after_print_rate_change():
    for print_instance in Print.objects.iterator(chunk_size=500):
        print_instance.save()
