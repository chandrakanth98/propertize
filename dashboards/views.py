from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views
from properties.models import InvitationCode
# Create your views here.

@login_required
def home(request):

    user = request.user


    if user.is_authenticated:
        if user.role == 1:
            return render(
                request,
                'dashboards/landlord.html'
            )
        elif user.role == 2:
            return render(
                request,
                'dashboards/contractor.html'
            )
        elif user.role == 3:
            return render(
                request,
                'dashboards/tenant.html'
            )
        elif user.role  == 0:
            return redirect('invite')
    else:
        return redirect('home')


@login_required
def invitation(request):
    if request.method == 'POST':
        invitation_code = request.POST.get('invitation_code')
        try:
            invitation = InvitationCode.objects.get(code=invitation_code)
            user = request.user
            user.role = 3
            user.assigned_property = invitation.property  # Assign property associated with the invitation code
            user.save()
            return redirect('home')
        except InvitationCode.DoesNotExist:
            # Handle invalid invitation code
            return render(request, 'dashboards/none.html', {'error': 'Invalid invitation code'})
    return render(request, 'dashboards/none.html')