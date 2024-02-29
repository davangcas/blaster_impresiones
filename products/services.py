from django.db.models import F, Sum


def calculate_product_price(product):
    current_price = 0
    current_price += (
        product.print_set.all()
        .annotate(prints_price=F("price"))
        .aggregate(Sum("prints_price"))["prints_price__sum"]
        or 0
    )
    current_price += (
        product.extra_costs.all()
        .annotate(extra_costs_price=F("cost"))
        .aggregate(Sum("extra_costs_price"))["extra_costs_price__sum"]
        or 0
    )
    return current_price
