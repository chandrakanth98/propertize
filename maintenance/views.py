from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm, EditMaintenanceForm, WorkerCodeForm
from .models import MaintenanceRequest, Worker
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
from .tables import MaintenanceRequestTable, WorkerCodeTable, ContractorTable
from .filters import MaintenanceFilter, WorkerFilter, ContractorFilter
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.contrib import messages
from properties.models import Property
from django.contrib.auth.decorators import login_required
User = get_user_model()


class MaintenanceTableView(SingleTableMixin, FilterView):
    """
    A view for displaying a table of maintenance requests.
    """

    table_class = MaintenanceRequestTable
    filterset_class = MaintenanceFilter
    paginate_by = 10
    template_name = 'maintenance/maintenance.html'


    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            for property in user.properties.all():
                maintenance_requests = MaintenanceRequest.objects.filter(
                    property=property)
                ordered_requests = maintenance_requests.order_by(
                    '-request_date')
                return ordered_requests

        elif user.role == 2:
            assigned_properties = Property.objects.filter(
                assigned_contractor=user)
            maintenance_requests = MaintenanceRequest.objects.filter(
                property__in=assigned_properties)
            ordered_requests = maintenance_requests.order_by('-request_date')
            return ordered_requests

            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role == 1:
            properties = user.properties.all()
        elif user.role == 2:
            properties = user.assigned_contractor.all()
        else:
            properties = Property.objects.none()

        context['properties'] = properties
        return context
    

@login_required
def maintenance_request(request, request_id):
    """
    View function for rendering individual maintenance request.
    """
    maintenance_request = get_object_or_404(MaintenanceRequest, request_id=request_id)
    user = request.user
    contractors = maintenance_request.property.assigned_contractor.all()
    print("Contractors:", contractors)

    if request.user not in [
        maintenance_request.submitted_by, maintenance_request.property.landlord, *contractors]:
        return HttpResponseNotFound()
    else:
        form = EditMaintenanceForm(
            instance=maintenance_request, contractors=contractors, user=user)
        if request.method == 'POST':
            form = EditMaintenanceForm(
                request.POST, instance=maintenance_request, contractors=contractors)
            if form.is_valid():
                form.save()
                messages.success(request, 'Maintenance request updated')
                return redirect('maintenance_request', request_id=request_id)
            else:
                messages.warning(request, 'An error occurred')
                print(form.errors)
                return redirect('maintenance_request', request_id=request_id)
    
    context = {'mr': maintenance_request, 'form': form, 'user': user}

    return render(request, 'maintenance/maintenance_request.html', context)


@login_required
def maintenance_form(request):
    """
    Renders a maintenance request form and handles form submission.
    """
    user = request.user
    properties = user.properties.all()

    if request.method == 'POST':
        form = MaintenanceForm(request.POST, user=user, properties=properties)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.submitted_by = user
            instance.save()
            messages.success(request, 'Maintenance request submitted')
            return redirect('maintenance_request', request_id=instance.request_id)
        else:
            messages.error(request, 'An error occurred')
            print(form.errors)
            return redirect('request')
    else:
        form = MaintenanceForm(user=user, properties=properties)
    return render(request, 'maintenance/request.html', {'form': form, 'user': user})


@login_required
def tenant_maintenance_request(request, user_id):
    """
    Tenant specific maintenance request view w/ form.
    """
    profile = get_object_or_404(User, pk=user_id)

    try:
        maintenance_requests = profile.submitted_by.all().order_by('-request_date')
    except ObjectDoesNotExist:
        maintenance_requests = None

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.submitted_by = profile
            instance.save()
            messages.success(request, 'Maintenance request submitted')
            return redirect('maintenance_request', request_id=instance.request_id)
        else:
            messages.error(request, 'An error occurred when submitting request')
            print(form.errors)
            return redirect('tenant_maintenance_request', user_id=user_id)
    else:
        form = MaintenanceForm(user=profile)

    context = {'maintenance': maintenance_requests,
                  'profile': profile,
                  'form': form}
    return render(request, 'maintenance/maintenance_user_request.html', context)


class WorkerTableView(SingleTableMixin, FilterView):
    """
    A view that displays a table of contractor codes and form to create them.
    """
    table_class = WorkerCodeTable
    template_name = 'maintenance/workers.html'
    filterset_class = WorkerFilter
    paginate_by = 5


    def get_queryset(self):
        user = self.request.user
        codes = Worker.objects.filter(assigned_properties__landlord=user).distinct()
        ordered_codes = codes.order_by('-created_on')
        return ordered_codes


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        form = WorkerCodeForm(user=user)
        context['form'] = form

        return context

        
    def post(self, request, *args, **kwargs):
        form = WorkerCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contractor code created')
            return redirect('workers')
        else:
            context = self.get_context_data()
            messages.error(request, 'An error occurred')
        return render(request, 'maintenance/workers.html', context)
    

class ContractorTableView(SingleTableMixin, FilterView):
    """
    A view that renders a table of contractors related to the user.
    """
    table_class = ContractorTable
    template_name = 'maintenance/contractors.html'
    filterset_class = ContractorFilter
    paginate_by = 10


    def get_queryset(self):
        user = self.request.user
        properties = user.properties.all()
        contractors = User.objects.filter(assigned_contractor__in=properties).distinct()
        ordered_contractors = contractors.order_by('first_name')
        return ordered_contractors


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        properties = user.properties.all()
        contractors = User.objects.filter(assigned_contractor__in=properties).distinct()
        form = WorkerCodeForm(user=user)
        context['contractors'] = contractors
        context['form'] = form

        return context
    

@login_required
def delete_invitation_contractor(request, code_id):
    """
    Deletes a specified contractor invitation code when called upon.
    """
    if request.user.role != 1:
        messages.error(request, 'You do not have permission to delete invitation codes!')
        return redirect('home')
    else:
        code = get_object_or_404(Worker, pk=code_id)
        code.delete()
        messages.success(request, 'Invitation code successfully deleted!')
    
    return redirect('workers')
