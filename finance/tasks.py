from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta
from calendar import monthrange
from tenants.models import Tenant
from finance.models import Transaction

@shared_task
def generate_rent_invoices():
    current_date = datetime.now().date()
    current_month_start = current_date.replace(day=1)
    current_month_end = current_date.replace(day=monthrange(current_date.year, current_date.month)[1])
    current_month_name = current_date.strftime("%B")
    

    for tenant in Tenant.objects.filter(is_active=True):

        if tenant.next_rent_due.month > current_month_end.month:
            continue

        if not tenant.current_rent_period_start or not tenant.current_rent_period_end:
            tenant.current_rent_period_end = tenant.next_rent_due
            tenant.current_rent_period_start = tenant.next_rent_due.replace(day=1)
            tenant.save()

        current_rent_start = tenant.current_rent_period_start

        due_date = current_month_end

        previous_month = current_month_start - timedelta(days=1)
        unpaid_transactions = Transaction.objects.filter(user=tenant.resident, due_date__year=previous_month.year, due_date__month=previous_month.month, status=0)

        if unpaid_transactions.exists():
            unpaid_amount = sum(transaction.amount for transaction in unpaid_transactions)
            tenant.outstanding_rent += unpaid_amount
            tenant.save()
            unpaid_transactions.update(status=2)


        transaction_exists = Transaction.objects.filter(user=tenant.resident, transaction_month=current_rent_start).exists()

        if not transaction_exists:
            total_amount = tenant.rent_amount + tenant.outstanding_rent + tenant.overdue_fee
            property = tenant.resident.assigned_property

            note = f"Rent invoice for {current_month_name}"
            transaction = Transaction.objects.create(
                user = tenant.resident,
                type=1,
                amount=total_amount,
                note=note,
                property=property,
                overdue_fee=tenant.overdue_fee,
                transaction_month=current_rent_start,
                due_date=due_date
            )
            transaction.save()


            tenant.current_rent_period_start = current_month_start
            tenant.current_rent_period_end = current_month_end
            tenant.outstanding_rent = 0
            tenant.save()

    for tenant in Tenant.objects.filter(is_active=True):
        tenant.next_rent_due = current_month_end
        tenant.save()
