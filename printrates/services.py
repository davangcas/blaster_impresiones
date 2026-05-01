from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Sum

from printrates.models import MonthlyCost, PrintRate, PrintRateVariables
from users.models import User


def obtain_print_rate():
    print_rate_variables = PrintRateVariables.get_singleton()
    daily_hours = Decimal(print_rate_variables.expected_daily_print_hours or 1)
    if daily_hours < 1:
        daily_hours = Decimal(1)
    expected_monthly_hours = daily_hours * Decimal(30)

    monthly_costs = MonthlyCost.objects.all().aggregate(Sum("cost"))[
        "cost__sum"
    ] or Decimal(0)
    salaries = User.objects.filter(is_active=True).aggregate(Sum("salary"))[
        "salary__sum"
    ] or Decimal(0)

    print_rate = (Decimal(monthly_costs) + Decimal(salaries)) / expected_monthly_hours
    return print_rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generate_print_rate():
    instance = PrintRate.get_singleton()
    instance.rate = obtain_print_rate()
    instance.save()
