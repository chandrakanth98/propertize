from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm, EditProfileForm, EditTenantForm, AddContractorCodeForm
from django.contrib.auth import get_user_model
from .tables import TenantTable, InvitationCodeTable
from properties.models import Tenant, Property, InvitationCode
from django_tables2 import SingleTableMixin
from .filters import TenantFilter, InvitationCodeFilter
from django_filters.views import FilterView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.contrib import messages
import cloudinary.uploader
from django.utils.safestring import mark_safe
from finance.models import Transaction
from maintenance.models import Worker

User = get_user_model()



class TenantTableView(SingleTableMixin, FilterView):
    """
    View for displaying a table of tenants associated with properties owned by the user.
    """
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

        



        return context

    template_name = "tenants/tenants.html"


@login_required
def profile(request, user_id):
    """
    View function for displaying a user's profile.
    """
    profile = get_object_or_404(User, pk=user_id)
    if request.user != profile and request.user.role != 1:
        return HttpResponseNotFound('test')

    try:
        tenant = Tenant.objects.get(resident=profile.user_id)
    except ObjectDoesNotExist:
        tenant = None

    try:
        transactions = profile.transaction.all().order_by('-due_date')[:3]
        for transaction in transactions:
            transaction.note = mark_safe(transaction.note)
    except ObjectDoesNotExist:
        transactions = None
    
    try:
        maintenance_requests = profile.submitted_by.all().order_by('-request_date')[:3]
    except ObjectDoesNotExist:
        maintenance_requests = None

    form1 = EditProfileForm(instance=profile)
    tenant = Tenant.objects.filter(resident=user_id).first()
    tenant_form = EditTenantForm(instance=tenant)
    add_contractor = AddContractorCodeForm()

    
    if request.method == 'POST':
        if request.user != profile and profile.assigned_property.landlord != request.user:
            messages.error(request, 'You can only edit your own profile!')
            return redirect('user_profile', user_id=user_id)
        else:
            form1 = EditProfileForm(request.POST, instance=profile)
            tenant_form = EditTenantForm(request.POST, instance=tenant)
            add_contractor = AddContractorCodeForm(request.POST)
            if 'form1' in request.POST and form1.is_valid():
                image = request.FILES.get('profile_image')
                if image:
                    upload_result = cloudinary.uploader.upload(image)
                    form1.instance.profile_image = upload_result['url']
                form1.save()
                messages.success(request, 'Profile successfully updated!')
                return redirect('user_profile', user_id=user_id)
            elif 'tenant_form' in request.POST and tenant_form.is_valid():
                if profile.assigned_property.landlord != request.user:
                    messages.error(request, 'You do not have permission to edit tenant details!')
                    return redirect('user_profile', user_id=user_id)
                else:
                    tenant_form.save()
                    messages.success(request, 'Tenant details successfully updated!')
                    return redirect('user_profile', user_id=user_id)
            elif 'add_contractor' in request.POST and add_contractor.is_valid():
                if profile.role == 2:
                    try:
                        worker_code = add_contractor.cleaned_data['code']
                        worker = Worker.objects.get(code=worker_code)
                        if worker.used:
                            messages.warning(request, 'Invitation code already used!')
                            return redirect('user_profile', user_id=user_id)
                        
                        user = request.user
                        for property in worker.assigned_properties.all():
                            if property.assigned_contractor.filter(pk=user_id).exists():
                                messages.warning(request, f'You are already assigned to {property.name}!')
                            else:
                                property.assigned_contractor.add(user)
                                worker.used = True
                                worker.save()
                                messages.success(request, f'You have been successfully assigned to {property.name}!')
                        return redirect('user_profile', user_id=user_id)
                        
                    except Worker.DoesNotExist:
                        messages.warning(request, 'Invalid invitation code')
                        return render(request, 'user_profile', user_id=user_id)
                else:
                    messages.error(request, 'You do not have permission to add contractor codes!')
                    return redirect('user_profile', user_id=user_id)
            else:
                messages.error(request, 'An error occurred while updating your profile!')
                print(form1.errors)
                print(tenant_form.errors)
                print(add_contractor.errors)
                return redirect('user_profile', user_id=user_id)



    context = {'profile': profile,
               'tenant': tenant,
               'transactions': transactions,
               'maintenance': maintenance_requests,
               'form1': form1,
               'tenant_form': tenant_form,
               'add_contractor': add_contractor}
    
    return render(request,
                  'tenants/profile.html',
                  context)



class CodeTableView(SingleTableMixin, FilterView):
    """
    View for displaying a table to render and a form to create
    tenant invitation codes.
    """
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
            messages.success(request, 'Invitation code successfully created!')
            return redirect('generate_code')
        else:
            context = self.get_context_data()
            context['form'] = form
            messages.error(request, 'An error occurred while creating the invitation code!')
        return render(request, self.template_name, context)


@login_required
def delete_invitation(request, code_id):
    """
    Deletes an invitation code.
    """
    if request.user.role != 1:
        messages.error(request, 'You do not have permission to delete invitation codes!')
        return redirect('home')
    else:
        code = get_object_or_404(InvitationCode, pk=code_id)
        code.delete()
        messages.success(request, 'Invitation code successfully deleted!')
    
    return redirect('generate_code')