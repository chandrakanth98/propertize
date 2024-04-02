from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm
from django.contrib.auth import get_user_model
from .tables import TenantTable, InvitationCodeTable
from properties.models import Tenant, Property, InvitationCode
from django_tables2 import SingleTableMixin
from .filters import TenantFilter, InvitationCodeFilter
from django_filters.views import FilterView

User = get_user_model()

# Create your views here.


# @login_required
# def tenants(request):
#     """
#     I DONT KNOW HOW THE FUCK I GOT HERE AFTER HOURS OF TRYING
#     TO GET THE TABLES TO RENDER THE CORRECT DATA BUT IT WORKS ?????
#     -----
#     This renders the properties and its tenants associated
#     with the logged in landlord / This logic was originally written to display 
#     all tenants grouped by property, hence the property key.
#     """
#     user = request.user
#     properties = Property.objects.filter(landlord=user)
#     property_tables = {}
#     total_tenants = 0
#     total_properties = properties.count()
    
    
#     for property in properties:
#         tenants_of_property = property.tenants.all()
#         tenant_objects = Tenant.objects.filter(resident__in=tenants_of_property)
#         total_tenants += tenant_objects.count()
#         table = TenantTable(tenant_objects)
#         property_tables[property] = table
    


#     context = {'property_tables': property_tables,
#                'total_tenants': total_tenants,
#                'total_properties': total_properties,
#                }
#     return render(
#         request,
#         'tenants/tenants.html',
#         context,
#     )


# def create_invitation_code(request):
#     user=request.user
#     if request.method == 'POST':
#         form = InvitationCodeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('tenants')
#     else:
#         form = InvitationCodeForm(user=user)
#     return render(request, 'tenants/generate.html', {'form': form})


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

    template_name = "tenants/tenants.html"


def profile(request, user_id):
    profile = get_object_or_404(User, pk=user_id)
    tenant = Tenant.objects.filter(resident=profile.user_id)
    context = {'profile': profile,
               'tenant': tenant}
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