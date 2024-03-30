from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm
from .tables import TenantTable
from properties.models import Tenant, Property
from django_tables2 import SingleTableMixin
from .filters import TenantFilter
from django_filters.views import FilterView


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


def create_invitation_code(request):
    user=request.user
    if request.method == 'POST':
        form = InvitationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenants')
    else:
        form = InvitationCodeForm(user=user)
    return render(request, 'tenants/generate.html', {'form': form})


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


def profile(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    context = {'tenant': tenant}
    return render(request,
                   'tenants/profile.html',
                     context)