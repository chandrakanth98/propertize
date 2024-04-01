from django.shortcuts import render
from finance.tasks import generate_rent_invoices

# Create your views here.

def finance(request):
    return render(request, "finance/finance.html")