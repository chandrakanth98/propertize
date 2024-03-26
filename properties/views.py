from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import views

# Create your views here.


@login_required
def properties(request):
    return render(
        request,
        'properties/properties.html',
    )