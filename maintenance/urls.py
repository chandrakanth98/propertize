from django.urls import path
from . import views


urlpatterns = [
    path('', views.maintenance, name='maintenance'),
    path('request/', views.maintenance_form, name='request'),
    path('request/<int:user_id>', views.tenant_maintenance_request, name='tenant_maintenance_request'),
]