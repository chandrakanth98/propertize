from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm, EditMaintenanceForm
from .models import MaintenanceRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotFound
User = get_user_model()

# Create your views here.

def maintenance(request):
    return render(request, 'maintenance/maintenance.html')

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