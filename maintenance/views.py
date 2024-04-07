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
User = get_user_model()

# Create your views here.


class MaintenanceTableView(SingleTableMixin, FilterView):
    table_class = MaintenanceRequestTable
    filterset_class = MaintenanceFilter
    paginate_by = 10
    template_name = 'maintenance/maintenance.html'

    def get_queryset(self):
        user = self.request.user
        if user.role == 1:
            for property in user.properties.all():
                maintenance_requests = MaintenanceRequest.objects.filter(property=property)
                ordered_requests = maintenance_requests.order_by('-request_date')
                return ordered_requests

        elif user.role == 2:
            assigned_properties = Property.objects.filter(assigned_contractor=user)
            maintenance_requests = MaintenanceRequest.objects.filter(property__in=assigned_properties)
            return maintenance_requests

            

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
    



def maintenance_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, request_id=request_id)
    user = request.user
    contractors = maintenance_request.property.assigned_contractor.all()
    print("Contractors:", contractors)

    if request.user != maintenance_request.submitted_by and request.user != maintenance_request.property.landlord and request.user not in contractors:
        return HttpResponseNotFound('test')
    else:
        form = EditMaintenanceForm(instance=maintenance_request, contractors=contractors, user=user)
        if request.method == 'POST':
            form = EditMaintenanceForm(request.POST, instance=maintenance_request, contractors=contractors)
            if form.is_valid():
                form.save()
                messages.success(request, 'Maintenance request updated')
                return redirect('maintenance_request', request_id=request_id)
            else:
                messages.error(request, 'An error occurred')
                print(form.errors)
                return redirect('maintenance_request', request_id=request_id)

    return render(request, 'maintenance/maintenance_request.html', {'mr': maintenance_request, 'form': form, 'user': user})

def maintenance_form(request):
    user=request.user
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.submitted_by = user
            instance.save()
            return redirect('home')
    else:
        form = MaintenanceForm(user=user)
    return render(request, 'maintenance/request.html', {'form': form, 'user': user})

def tenant_maintenance_request(request, user_id):
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
            return redirect('home')
    else:
        form = MaintenanceForm(user=profile)

    context = {'maintenance': maintenance_requests,
                  'profile': profile,
                  'form': form}
    return render(request, 'maintenance/maintenance_user_request.html', context)


class WorkerTableView(SingleTableMixin, FilterView):
    table_class = WorkerCodeTable
    template_name = 'maintenance/workers.html'
    filterset_class = WorkerFilter
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        codes = Worker.objects.filter(assigned_properties__landlord=user).distinct()
        ordered_codes = codes.order_by('-used')
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
            messages.success(request, 'Worker code created')
            return redirect('workers')
        else:
            context = self.get_context_data()
            messages.error(request, 'An error occurred')
        return render(request, 'maintenance/workers.html', context)
    

class ContractorTableView(SingleTableMixin, FilterView):
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
