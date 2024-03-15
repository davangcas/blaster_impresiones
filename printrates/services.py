from decimal import Decimal

from django.db.models import Sum

from printrates.models import MonthlyCost, PrintRate, PrintRateVariables
from users.models import User


def obtain_print_rate():
    print_rate = Decimal(0)
    month_days = Decimal(30)
    available_printers = Decimal(1)
    print_rate_variables = PrintRateVariables.objects.order_by("-created_at").first()

    if print_rate_variables:
        available_printers = print_rate_variables.available_printers

    monthly_costs = MonthlyCost.objects.all().aggregate(Sum("cost"))["cost__sum"] or 0
    print_rate += (monthly_costs / month_days) / 24 / available_printers
    salaries = (
        User.objects.filter(is_active=True).aggregate(Sum("salary"))["salary__sum"] or 0
    )
    print_rate += (salaries / month_days) / 8 / available_printers
    print_rate = print_rate.quantize(Decimal("0.01"))
    return print_rate


def generate_print_rate():
    PrintRate.objects.create(rate=obtain_print_rate())
