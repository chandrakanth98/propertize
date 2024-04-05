from django.shortcuts import render
from finance.tasks import generate_rent_invoices
from django.http import HttpResponse
from .models import Transaction
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import TransactionTable
from .filters import TransactionFilter
from tenants.models import Tenant



# Create your views here.

def finance(request):
    generate_rent_invoices()
    return render(request, "finance/finance_overview.html")


class TransactionListView(SingleTableMixin, FilterView):
    table_class = TransactionTable
    filterset_class = TransactionFilter
    template_name = 'finance/transaction_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            ordered_transactions = Transaction.objects.filter(property__in=user.properties.all()).order_by('-due_date')
            return ordered_transactions
        elif user.role == 3:
            ordered_transactions = Transaction.objects.filter(user=user).order_by('-due_date')
            return ordered_transactions
        
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.filter(transaction_id=transaction_id).first()
    tenant = Tenant.objects.filter(resident=transaction.user).first()
    return render(request, 'finance/transaction_detail.html', {'transaction': transaction, 'tenant': tenant})
