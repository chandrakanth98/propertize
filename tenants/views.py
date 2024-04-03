from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm
from django.contrib.auth import get_user_model
from .tables import TenantTable, InvitationCodeTable
from properties.models import Tenant, Property, InvitationCode
from django_tables2 import SingleTableMixin
from .filters import TenantFilter, InvitationCodeFilter
from django_filters.views import FilterView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound

User = get_user_model()

class TenantTableView(SingleTableMixin, FilterView):
    table_class = TenantTable
    filterset_class = TenantFilter
    paginate_by = 15

    def get_queryset(self):
        user = self.request.user
        properties = Property.objects.filter(landlord=user)
        tenant_objects = Tenant.objects.none()

        for property in properties:
            tenants_of_property = property.tenants.all()
            tenant_objects |= Tenant.objects.filter(resident__in=tenants_of_property)

        ordered_tenants = tenant_objects.order_by('resident__first_name')

        return ordered_tenants
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        properties = Property.objects.filter(landlord=user)
        tenants = Tenant.objects.none()
        expense = Property.objects.none()

        for property in properties:
            tenants |= property.tenants.all()
            expense |= property.transactions.filter(type=2)

        context['expense'] = expense
        context['tenants'] = tenants
        context['properties'] = properties
        return context

    template_name = "tenants/tenants.html"


def profile(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    if request.user != profile and request.user.role != 1:
        return HttpResponseNotFound('test')

    try:
        tenant = Tenant.objects.get(resident=profile.user_id)
    except ObjectDoesNotExist:
        tenant = None

    try:
        transactions = profile.transaction.all().order_by('-due_date')[:3]
    except ObjectDoesNotExist:
        transactions = None
    
    try:
        maintenance_requests = profile.submitted_by.all().order_by('-request_date')[:3]
    except ObjectDoesNotExist:
        maintenance_requests = None

    context = {'profile': profile,
               'tenant': tenant,
               'transactions': transactions,
               'maintenance': maintenance_requests}
    
    return render(request,
                  'tenants/profile.html',
                  context)

class CodeTableView(SingleTableMixin, FilterView):
    table_class = InvitationCodeTable
    filterset_class = InvitationCodeFilter
    paginate_by = 15
    template_name = "tenants/generate.html"

    def get_queryset(self):
        user = self.request.user
        properties = Property.objects.filter(landlord=user)
        code_objects = InvitationCode.objects.none()

        for property in properties:
            code_objects |= InvitationCode.objects.filter(property__in=properties)

        ordered_codes = code_objects.order_by('-created_at')

        return ordered_codes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InvitationCodeForm(user=self.request.user)
        return context
    
    def post(self, request):
        form = InvitationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_code')
        else:
            context = self.get_context_data()
            context['form'] = form
        return render(request, self.template_name, context)