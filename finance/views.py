from django.shortcuts import render, redirect
from finance.tasks import generate_rent_invoices
from django.http import HttpResponse
from .models import Transaction
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import TransactionTable
from .filters import TransactionFilter
from tenants.models import Tenant
from .forms import EditTransactionForm, CreateTransactionForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required
def finance(request):
    generate_rent_invoices()
    return render(request, "finance/finance_overview.html")



class TransactionListView(SingleTableMixin, FilterView):
    """
    View for displaying a list of all transactions related to user.
    """
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


@login_required        
def transaction_detail(request, transaction_id):
    """
    View function for displaying individual transaction.
    """
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


@login_required
def transaction_form(request):
    """
    Renders a form for creating a transaction and POSTing it.
    """
    user=request.user
    User = get_user_model()


    def get_queryset():
        """
        Retrieves the queryset of tenants and properties based on the user's
        role and related properties.
        """
        if user.role == 1:
            properties = user.properties.filter(landlord=user)
        elif user.role == 2:
            properties = user.assigned_contractor.all()
        tenant_objects = User.objects.none()

        for property in properties:
            tenants_of_property = property.tenants.all()
            tenant_objects |= User.objects.filter(user_id__in=tenants_of_property)

        tenants = tenant_objects.order_by('first_name')

        return tenants, properties

    tenants, properties = get_queryset()

    if request.method == 'POST':
        if user.role == 1 or user.role == 2:
            form = CreateTransactionForm(request.POST, tenants=tenants, properties=properties)
            if form.is_valid():
                transaction = form.save(commit=False)
                if not transaction.user:
                    transaction.user = user
                transaction.save()
                transaction_id = transaction.transaction_id
                messages.success(request, 'Transaction created successfully.')
                return redirect('transaction_detail', transaction_id=transaction_id)
            else:
                messages.error(request, 'There was an error creating the transaction.')
                print(form.errors)
                return render(request, 'finance/transaction_form.html', {'form': form})

        else:
            messages.warning(request, 'You do not have permission to create a transaction.')
            return redirect('transaction_list')

    else:
        form = CreateTransactionForm(user=user, tenants=tenants, properties=properties)
        return render(request, 'finance/transaction_form.html', {'form': form})
