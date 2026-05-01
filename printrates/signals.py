from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from printrates.models import MonthlyCost, PrintRate, PrintRateVariables
from printrates.services import generate_print_rate
from printrates.tasks import refresh_prints_after_print_rate_change


@receiver(post_save, sender=PrintRate)
def print_rate_post_save(sender, instance, **kwargs):
    refresh_prints_after_print_rate_change.delay()


@receiver(post_delete, sender=PrintRate)
def print_rate_post_delete(sender, instance, **kwargs):
    # Singleton: si por error se elimina la instancia, recalculamos precios de prints
    # (get_singleton() creará una nueva instancia en la siguiente petición)
    refresh_prints_after_print_rate_change.delay()


@receiver(post_save, sender=PrintRateVariables)
def print_rate_variables_post_save(sender, instance, **kwargs):
    generate_print_rate()


@receiver(post_delete, sender=PrintRateVariables)
def print_rate_variables_post_delete(sender, instance, **kwargs):
    generate_print_rate()


@receiver(post_save, sender=MonthlyCost)
def monthly_cost_post_save(sender, instance, **kwargs):
    generate_print_rate()


@receiver(post_delete, sender=MonthlyCost)
def monthly_cost_post_delete(sender, instance, **kwargs):
    generate_print_rate()
