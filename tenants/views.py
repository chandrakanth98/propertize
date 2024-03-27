from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import InvitationCodeForm

# Create your views here.

@login_required
def tenants(request):
    return render(
        request,
        'tenants/tenants.html',
    )

def create_invitation_code(request):
    user=request.user
    if request.method == 'POST':
        form = InvitationCodeForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('tenants')
    else:
        form = InvitationCodeForm(user=user)
    return render(request, 'tenants/generate.html', {'form': form})