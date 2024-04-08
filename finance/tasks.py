from celery import shared_task
from calendar import monthrange
from datetime import datetime, timedelta

from tenants.models import Tenant
from finance.models import Transaction


@shared_task
def generate_rent_invoices():
    """
    Generates rent invoices for active tenants based on the current date.
    The function calculates the current month's start and end dates, as well as the next month's end date.
    It then iterates over each active tenant and performs the following steps:
    - If the tenant's current rent period start or end dates are not set, they are updated based on the next rent due date.
    - If the tenant's next rent due date is in a future month, the iteration continues to the next tenant.
    - Any unpaid transactions from the previous month are checked for overdue fees. If the overdue days exceed the tenant's overdue fee days,
      the transaction status is updated, and the tenant's outstanding rent and overdue status are updated accordingly.
    - If there are unpaid transactions from the previous month that are not overdue, the iteration continues to the next tenant.
    - If there are no existing transactions for the current month, a new transaction is created for the tenant with the rent amount,
      outstanding rent, and any overdue fees. The tenant's rent period start, end, and next rent due dates are updated, and the outstanding rent
      and overdue status are reset.
    """
    current_date = datetime.now().date()
    current_month_start = current_date.replace(day=1)
    current_month_end = current_date.replace(day=monthrange(current_date.year, current_date.month)[1])
    current_month_name = current_date.strftime("%B")
    next_month = current_date.replace(month=current_date.month + 1)
    next_month_end = next_month.replace(day=monthrange(next_month.year, next_month.month)[1])
    

    for tenant in Tenant.objects.filter(is_active=True):

        if not tenant.current_rent_period_start or not tenant.current_rent_period_end:
            tenant.current_rent_period_end = tenant.next_rent_due
            tenant.current_rent_period_start = tenant.next_rent_due.replace(day=1)
            tenant.save()

        if tenant.next_rent_due.month > current_month_end.month:
            continue

        due_date = current_month_end

        previous_month = current_month_start - timedelta(days=1)
        unpaid_transactions = Transaction.objects.filter(user=tenant.resident, due_date__year=previous_month.year, due_date__month=previous_month.month, status=0, note__startswith="Rent invoice for")

        if unpaid_transactions.exists():
            for transaction in unpaid_transactions:
                overdue_days = (current_date - transaction.due_date).days
                if overdue_days > tenant.overdue_fee_days:
                    transaction.status = 2
                    transaction.save()
                    tenant.outstanding_rent += transaction.amount
                    tenant.overdue = True
                    tenant.save()
                else:
                    continue

        unpaid_transactions = Transaction.objects.filter(user=tenant.resident, due_date__year=previous_month.year, due_date__month=previous_month.month, status=0, note__startswith="Rent invoice for")
        unpaid_not_overdue = False
        for transaction in unpaid_transactions:
            overdue_days = (current_date - transaction.due_date).days
            if overdue_days <= tenant.overdue_fee_days:
                unpaid_not_overdue = True
                break

        if unpaid_not_overdue:
            continue

        transaction_exists = Transaction.objects.filter(user=tenant.resident, transaction_month=current_month_start, status__in=[0, 1, 2], note__startswith="Rent invoice for").exists()
        if not transaction_exists:
            tenant.rent_amount = max(0, tenant.rent_amount)
            total_amount = tenant.rent_amount + tenant.outstanding_rent
            property = tenant.resident.assigned_property

            note = f"Rent invoice for {current_month_name}"
            if tenant.overdue:
                note += "<br>" + "(Outstanding Balance)" + "<br>" + f"Overdue amount: {tenant.outstanding_rent}" + "<br>" + f"Overdue fee: {tenant.overdue_fee}"
                total_amount += tenant.overdue_fee
            transaction = Transaction.objects.create(
                user = tenant.resident,
                type=1,
                amount=total_amount,
                note=note,
                property=property,
                transaction_month=current_month_start,
                due_date=due_date
            )
            transaction.save()

            tenant.current_rent_period_start = current_month_start
            tenant.current_rent_period_end = current_month_end
            tenant.next_rent_due = next_month_end
            tenant.outstanding_rent = 0
            tenant.overdue = False
            tenant.save()
