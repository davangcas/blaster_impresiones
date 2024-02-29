from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from printrates.models import PrintRate, PrintRateVariables, MonthlyCost
from prints.models import Print
from printrates.services import update_print_rate


@receiver(post_save, sender=PrintRate)
def print_rate_post_save(sender, instance, **kwargs):
    all_prints = Print.objects.all()

    for print_instance in all_prints:
        print_instance.save()


@receiver(post_delete, sender=PrintRate)
def print_rate_post_delete(sender, instance, **kwargs):
    if PrintRate.objects.count() != 0:
        all_prints = Print.objects.all()

        for print_instance in all_prints:
            print_instance.save()


@receiver(post_save, sender=PrintRateVariables)
def print_rate_variables_post_save(sender, instance, **kwargs):
    update_print_rate()


@receiver(post_delete, sender=PrintRateVariables)
def print_rate_variables_post_delete(sender, instance, **kwargs):
    update_print_rate()


@receiver(post_save, sender=MonthlyCost)
def monthly_cost_post_save(sender, instance, **kwargs):
    update_print_rate()


@receiver(post_delete, sender=MonthlyCost)
def monthly_cost_post_delete(sender, instance, **kwargs):
    update_print_rate()
