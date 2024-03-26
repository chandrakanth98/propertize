from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views
# Create your views here.

@login_required
def home(request):


    if request.user.is_authenticated:
        if request.user.role == 1:
            return render(
                request,
                'dashboards/landlord.html'
            )
        elif request.user.role == 2:
            return render(
                request,
                'dashboards/contractor.html'
            )
        elif request.user.role == 3:
            return render(
                request,
                'dashboards/tenant.html'
            )
    else:
        return render(
            request,
            'dashboards/none.html'
        )