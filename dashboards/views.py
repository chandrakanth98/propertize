from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views
from tenants.views import profile
from properties.models import InvitationCode
from tenants.models import Tenant
# Create your views here.

@login_required
def home(request):

    user = request.user
    user_id = request.user.user_id


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
            return redirect('user_profile', user_id=user_id)
        
        elif user.role  == 0:
            return redirect('invite')
    else:
        return redirect('home')


@login_required
def invitation(request):
    if request.method == 'POST':
        invitation_code = request.POST.get('invitation_code')
        try:
            invitation = InvitationCode.objects.get(code=invitation_code, used=False)
            user = request.user
            user.role = 3
            user.assigned_property = invitation.property
            tenant = Tenant.objects.create(
                resident=user,
                rent_amount=invitation.rent_amount,
                lease_end=invitation.lease_end,
                next_rent_due=invitation.next_rent_due,
                apartment=invitation.apartment,
            )
            tenant.save()
            user.save()
            invitation.used = True
            invitation.save()
            return redirect('home')
        except InvitationCode.DoesNotExist:
            # Handle invalid invitation code
            return render(request, 'dashboards/none.html', {'error': 'Invalid invitation code'})
    return render(request, 'dashboards/none.html')