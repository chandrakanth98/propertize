from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views
from properties.models import Property, Tenant
from properties.forms import PropertyNoticeForm, EditProperty
from properties.tables import CustomTenantTable
from tenants.filters import TenantFilter
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib import messages


# Create your views here.


@login_required
def properties(request):
    return render(
        request,
        'properties/properties.html',
    )




class PropertyTenantTableView(SingleTableMixin, FilterView):
    table_class = CustomTenantTable
    filterset_class = TenantFilter
    paginate_by = 5
    template_name = "properties/property.html"

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        properties = Property.objects.filter(property_id=property_id)
        tenant_objects = Tenant.objects.none()

        for property in properties:
            tenants_of_property = property.tenants.all()
            tenant_objects |= Tenant.objects.filter(resident__in=tenants_of_property)

        ordered_tenants = tenant_objects.order_by('resident__first_name')

        return ordered_tenants
    
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PropertyNoticeForm(user=self.request.user)

        property_id = self.kwargs.get('property_id')
        property = Property.objects.get(pk=property_id)
        context['property'] = property
        context['edit_form'] = EditProperty(instance=property)

        latest_notices = property.property_notice.all().order_by('-posted_at')[:10]
        context['latest_notices'] = latest_notices
        context['property_id'] = property_id
        return context
    
    def post(self, request, property_id):
        form1 = PropertyNoticeForm(request.POST or None)
        form2 = EditProperty(request.POST or None, instance=Property.objects.get(pk=property_id))

        if 'form1' in request.POST and form1.is_valid():
            form1.save()
            messages.success(request, 'Notice successfully posted!')
            return redirect('property', property_id=property_id)
        elif 'form2' in request.POST and form2.is_valid():
            form2.save()
            messages.success(request, 'Property successfully edited!')
            return redirect('property', property_id=property_id)

        context = self.get_context_data()
        context['form'] = form1
        context['edit_form'] = form2
        return render(request, self.template_name, context)