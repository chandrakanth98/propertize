from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaintenanceForm
from .models import MaintenanceRequest

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

def maintenance_request(request, request_id):

    req = get_object_or_404(MaintenanceRequest, pk=request_id)
    context = {'req': req}
    return render(request, 'maintenance/maintenance_request.html', context)