from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm
from .tables import TenantTable
from properties.models import Tenant, Property


# Create your views here.

@login_required
def tenants(request):
    """
    I DONT KNOW HOW THE FUCK I GOT HERE AFTER HOURS OF TRYING
    TO GET THE TABLES TO RENDER THE CORRECT DATA BUT IT WORKS ?????
    -----
    This renders the properties and its tenants associated
    with the logged in landlord
    """
    user = request.user
    properties = Property.objects.filter(landlord=user)
    property_tables = {}
    
    for property in properties:
        tenants_of_property = property.tenants.all()
        tenant_objects = Tenant.objects.filter(resident__in=tenants_of_property)
        table = TenantTable(tenant_objects)
        property_tables[property] = table
    
    context = {'property_tables': property_tables}
    return render(
        request,
        'tenants/tenants.html',
        context,
    )


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
