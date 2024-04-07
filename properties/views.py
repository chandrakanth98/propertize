from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views
from properties.models import Property, Tenant
from properties.forms import PropertyNoticeForm, EditProperty, addProperty
from properties.tables import CustomTenantTable
from tenants.filters import TenantFilter
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib import messages
import cloudinary.uploader


# Create your views here.


@login_required
def properties(request):
    """
    View function for displaying and creating properties.
    """
    
    if request.user.role == 1:
        properties = Property.objects.filter(landlord=request.user).order_by('name')
        if request.method == 'POST':
            post = request.POST.copy()
            post['landlord'] = request.user.user_id
            form = addProperty(post, request.FILES)
            if form.is_valid():
                form.instance.landlord = request.user
                form.save()
                messages.success(request, 'Property successfully created!')
                return redirect('property', property_id=form.instance.property_id)
            else:
                messages.warning(request, 'Property could not be created!')
                print(form.errors)
        else:
            form = addProperty()
            return render(request, 'properties/properties.html', {'form': form, 'properties': properties})
    elif request.user.role == 2:
        form = addProperty()
        properties = Property.objects.filter(assigned_contractor=request.user)
        return render(request, 'properties/properties.html', {'form': form, 'properties': properties})
    else:
        messages.error(request, 'You do not have permission to create properties!')    
        form = None
        
    context = {'form': form}
    return render(request, 'properties/properties.html', context)


@login_required
def property_delete(request, property_id):
    """
    Delete a property.
    """
    property = get_object_or_404(Property, pk=property_id)

    if property.landlord == request.user:
        property.delete()
        messages.add_message(request, messages.SUCCESS, f'{property} was successfully deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own properties!')

    return redirect('properties')


class PropertyTenantTableView(SingleTableMixin, FilterView):
    """
    View for displaying a specific property and table of tenants for that property.
    
    """

    table_class = CustomTenantTable
    filterset_class = TenantFilter
    paginate_by = 5
    template_name = "properties/property.html"

    def get_queryset(self):
        """
        Returns the queryset of active tenants for the specified property.
        """
        property_id = self.kwargs.get('property_id')
        property_instance = get_object_or_404(Property, pk=property_id)
        
        tenants_of_property = property_instance.tenants.all()
        active_tenants = Tenant.objects.filter(resident__in=tenants_of_property, is_active=True)
        
        ordered_tenants = active_tenants.order_by('resident__last_name')
        
        return ordered_tenants
    
 
    def get_context_data(self, **kwargs):
        """
        Returns the context data for rendering the template.
        """
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
        """
        Handles the POST request for creating a property notice or editing a property.
        """
        form1 = PropertyNoticeForm(request.POST)
        property_instance = Property.objects.get(pk=property_id)
        form2 = EditProperty(request.POST, instance=property_instance)
        if property_instance.landlord == request.user:

            if 'form1' in request.POST and form1.is_valid():
                form1.save()
                messages.success(request, 'Notice successfully posted!')
                return redirect('property', property_id=property_id)
            
            elif 'form2' in request.POST and form2.is_valid():
                image = request.FILES.get('featured_image')
                if image:
                    upload_result = cloudinary.uploader.upload(image)
                    form2.instance.featured_image = upload_result['url']
                form2.save()
                messages.success(request, 'Property successfully edited!')
                return redirect('property', property_id=property_id)
        else:
            messages.error(request, 'You can only edit your own properties!')

        context = self.get_context_data()
        context['form'] = form1
        context['edit_form'] = form2
        return render(request, self.template_name, context)