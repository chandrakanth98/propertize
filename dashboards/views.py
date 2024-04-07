from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from properties.models import InvitationCode, Property, PropertyNotice
from maintenance.models import Worker, MaintenanceRequest
from tenants.models import Tenant
from finance.models import Transaction
from django.db.models import Sum
from django.contrib import messages


@login_required
def home(request):
    """
    Renders the home page based on the user's role.
    """

    user = request.user
    user_id = request.user.user_id

    if user.is_authenticated:
        if user.role == 1:
            # Landlord role

            properties = Property.objects.filter(landlord=user)

            tenants = Tenant.objects.none()
            transactions = Transaction.objects.filter(
                property__in=properties).order_by('-created_on')[:4]

            expense_trans = Transaction.objects.filter(
                property__in=properties, type=2, status=0)
            
            expense_total = expense_trans.aggregate(
                amount_sum=Sum('amount'))['amount_sum']
            
            expense = round(expense_total) if expense_total else 0

            latest_requests = MaintenanceRequest.objects.filter(
                property__in=properties).order_by('-request_date')[:4]
            
            latest_notices = PropertyNotice.objects.filter(
                property__in=properties).order_by('-posted_at')[:4]

            for property in properties:
                tenants = tenants.union(property.tenants.all())

            overdue_total = 0
            rent_total = 0
            for tenant in tenants:
                for resident in tenant.resident.all():
                    if resident.is_active:
                        overdue_total += (resident.outstanding_rent 
                                          if resident.outstanding_rent else 0)
                        rent_total += (resident.rent_amount 
                                       if resident.rent_amount else 0)

            rent_total = round(rent_total) if rent_total else 0
            overdue = round(overdue_total) if overdue_total else 0

            context = {
                'transactions': transactions,
                'latest_notices': latest_notices,
                'latest_requests': latest_requests,
                'invoice': expense_trans,
                'overdue': overdue,
                'rent_total': rent_total,
                'expense': expense,
                'tenants': tenants,
                'properties': properties,
            }

            return render(
                request,
                'dashboards/landlord.html',
                context
            )
        elif user.role == 2:
            # Property manager role
            return redirect('maintenance')
        elif user.role == 3:
            # Tenant role
            try:
                tenant = Tenant.objects.get(resident=user)

                if tenant.is_active:
                    return redirect('user_profile', user_id=user_id)
                else:
                    messages.warning(request, 'Your account is not active')
                    return render(
                        request,
                        'dashboards/none.html'
                    )
            except Tenant.DoesNotExist:
                raise Tenant.DoesNotExist("The tenant does not exist.")
        elif user.role == 0:
            # No role
            return redirect('invite')
    else:
        # User is not authenticated
        return redirect('home')


@login_required
def invitation(request):
    """
    Process the invitation code submitted by the user and perform the necessary
    actions based on tenant or constructor code.
    """
    if request.method == 'POST':
        if request.user.role == 0:
            invitation_code = request.POST.get('invitation_code')
            user = request.user

            try:
                invitation = InvitationCode.objects.get(code=invitation_code, used=False)
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
                messages.success(request, 'Invitation code used successfully, you are now a tenant')
                return redirect('home')
            
            except InvitationCode.DoesNotExist:
                pass

            try:
                worker = Worker.objects.get(code=invitation_code, used=False)
                user.role = 2
                user.save()
                for property in worker.assigned_properties.all():
                    property.assigned_contractor.add(user)
                worker.used = True
                worker.save()
                messages.success(request, 'Invitation code used successfully, you are now a contractor')
                return redirect('home')
            except Worker.DoesNotExist:
                pass

            messages.warning(request, 'Invalid invitation code')
            return render(request, 'dashboards/none.html')
        
        else:
            messages.warning(request, 'You do not have permission to use an invitation code')
            return redirect('home')
    
    else:
        return render(request, 'dashboards/none.html')
