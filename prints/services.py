from decimal import ROUND_HALF_UP, Decimal

from printrates.models import PrintRate, PrintRateVariables


def calculate_print_price(print_instance):
    current_price = 0
    material_cost = print_instance.material.price / 1000
    current_price += material_cost * print_instance.grams
    print_rate_instance = PrintRate.objects.order_by("-created_at").first()
    print_rate_variables = PrintRateVariables.objects.order_by("-created_at").first()
    print_rate = 0

    if print_rate_instance:
        print_rate = print_rate_instance.rate

    print_rate_in_minutes = print_rate / 60
    print_time = (print_instance.hours * 60) + print_instance.minutes
    current_price += print_time * Decimal(print_rate_in_minutes)

    if print_rate_variables:
        current_price *= (
            1
            + Decimal(print_rate_variables.failure_percentage).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            / 100
        )
        current_price *= (
            1
            + Decimal(print_rate_variables.extra_percentage).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            / 100
        )
        current_price += print_rate_variables.maintenance_cost
        current_price += (
            print_rate_variables.minutes_spent_per_print * print_rate_in_minutes
        )

    current_price = current_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    current_price = round(current_price / 10) * 10
    return current_price
