from django.urls import path
from . import views


urlpatterns = [
    path('', views.TenantTableView.as_view(), name='tenants'),
    path('generate/', views.CodeTableView.as_view(), name='generate_code'),
    path('profile/<int:tenant_id>', views.profile, name='user_profile'),
]