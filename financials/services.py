from django.db.models import Sum

from financials.choices import ACCOUNT_TYPES
from financials.models import Account, Transaction
from printrates.models import MonthlyCost
from users.models import User


def distribute_payment(order_instance):
    organization_account = Account.objects.get_or_create(
        user=None, name="blaster", account_type=ACCOUNT_TYPES[0][0]
    )[0]
    sale_transaction = Transaction.objects.create(
        to_account=organization_account,
        amount=order_instance.get_total_cost(),
        description=f"Venta de productos - {order_instance}",
    )

    total_salaries_amount = (
        User.objects.filter(is_active=True).aggregate(Sum("salary"))["salary__sum"] or 0
    )
    total_organization_amount = (
        MonthlyCost.objects.aggregate(Sum("cost"))["cost__sum"] or 0
    )
    total_monthly_amount = total_salaries_amount + total_organization_amount
    total_salaries_amount_percentage = 0

    if total_monthly_amount > 0:
        total_salaries_amount_percentage = total_salaries_amount / (
            total_salaries_amount + total_organization_amount
        )

    for user in User.objects.filter(is_active=True):
        account = Account.objects.get_or_create(
            user=user, name=user.username, account_type=ACCOUNT_TYPES[1][0]
        )[0]
        salary_percentage = 0

        if total_salaries_amount > 0:
            salary_percentage = user.salary / total_salaries_amount

        salary_amount = (
            sale_transaction.amount
            * total_salaries_amount_percentage
            * salary_percentage
        )
        Transaction.objects.create(
            from_account=organization_account,
            to_account=account,
            amount=salary_amount,
            description=f"Pago de salario - {order_instance}",
        )
