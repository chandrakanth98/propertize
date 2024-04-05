from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm, EditMaintenanceForm
from .models import MaintenanceRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
from .tables import MaintenanceRequestTable
from .filters import MaintenanceFilter
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
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
            maintenance_requests = MaintenanceRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        properties = user.properties.all()

        context['properties'] = properties
        return context
    



def maintenance_request(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, request_id=request_id)

    if request.user != maintenance_request.submitted_by and request.user.role != 2 and request.user.role != 1:
        return HttpResponseNotFound('test')
    else:
        form = EditMaintenanceForm(instance=maintenance_request)
        if request.method == 'POST':
            form = EditMaintenanceForm(request.POST, instance=maintenance_request)
            if form.is_valid():
                form.save()
                return redirect('maintenance_request', request_id=request_id)

    return render(request, 'maintenance/maintenance_request.html', {'mr': maintenance_request, 'form': form})

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
    return render(request, 'maintenance/request.html', {'form': form})

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