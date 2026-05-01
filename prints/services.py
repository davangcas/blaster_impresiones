from decimal import ROUND_HALF_UP, Decimal

from printrates.models import PrintRate, PrintRateVariables


def calculate_print_price(print_instance):
    variables = PrintRateVariables.get_singleton()
    rate_per_hour = PrintRate.get_singleton().rate
    rate_per_minute = rate_per_hour / Decimal(60)

    material_cost = (print_instance.material.price / Decimal(1000)) * Decimal(
        print_instance.grams
    )
    print_minutes = Decimal((print_instance.hours * 60) + print_instance.minutes)
    time_cost = print_minutes * rate_per_minute
    operator_cost = Decimal(variables.minutes_spent_per_print) * rate_per_minute

    direct_cost = material_cost + time_cost + operator_cost + variables.maintenance_cost
    cost_with_failures = direct_cost * (
        Decimal(1) + Decimal(variables.failure_percentage) / Decimal(100)
    )
    total_cost = cost_with_failures * (
        Decimal(1) + Decimal(variables.extra_percentage) / Decimal(100)
    )
    final_price = total_cost * (
        Decimal(1) + Decimal(variables.general_profit_margin) / Decimal(100)
    )

    final_price = final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal(round(final_price / 10) * 10)
