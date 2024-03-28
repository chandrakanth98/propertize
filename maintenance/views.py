from django.shortcuts import render, redirect
from .forms import MaintenanceForm

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