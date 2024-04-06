from django.urls import path
from . import views


urlpatterns = [
    path('', views.MaintenanceTableView.as_view(), name='maintenance'),
    path('request/', views.maintenance_form, name='request'),
    path('request/<int:request_id>', views.maintenance_request, name='maintenance_request'),
    path('request/tenant/<int:user_id>', views.tenant_maintenance_request, name='tenant_maintenance_request'),
    path('worker/', views.WorkerTableView.as_view(), name='workers'),
    path('contractor/', views.ContractorTableView.as_view(), name='contractors'),
]