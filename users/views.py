from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def custom404(request, exception):
    """
    Custom view to render my 404 page.
    """
    return render(request, '404.html', status=404)