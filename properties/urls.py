from django.urls import path
from . import views


urlpatterns = [
    path('', views.properties, name='properties'),
    path('property/<int:property_id>', views.PropertyTenantTableView.as_view(), name='property'),
    path('delete_property/<int:property_id>', views.property_delete, name='delete_property'),
]