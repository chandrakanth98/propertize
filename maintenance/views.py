from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm
from .models import MaintenanceRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def maintenance(request):
    return render(request, 'maintenance/maintenance.html')

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
    return render(request, 'maintenance/maintenance_request.html', context)