from django.shortcuts import render
from finance.tasks import generate_rent_invoices
from django.http import HttpResponse
from .models import Transaction
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import TransactionTable
from .filters import TransactionFilter
from tenants.models import Tenant
from .forms import EditTransactionForm
from django.contrib import messages



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
    form = EditTransactionForm(instance=transaction)

    context = {'transaction': transaction, 
               'tenant': tenant, 
               'form': form}

    if request.method == 'POST':
        form = EditTransactionForm(request.POST, instance=transaction)
        if request.user.role == 1:
            if form.is_valid():
                form.save()
                messages.success(request, 'Transaction updated successfully.')
                return render(request, 'finance/transaction_detail.html', context)
            else:
                messages.error(request, 'There was an error updating the transaction.')
                return render(request, 'finance/transaction_detail.html', context)
        else:
            messages.warning(request, 'You do not have permission to edit this transaction.')
            return render(request, 'finance/transaction_detail.html', context)

    return render(request, 'finance/transaction_detail.html', context)
