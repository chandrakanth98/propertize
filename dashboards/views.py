from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import views
# Create your views here.

@login_required
def home(request):

    return render(
        request,
        'dashboards/index.html'
    )