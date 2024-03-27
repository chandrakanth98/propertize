from django.urls import path
from . import views


urlpatterns = [
    path('', views.tenants, name='tenants'),
    path('generate', views.create_invitation_code, name='generate_code'),
]