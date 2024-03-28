from django.urls import path
from . import views


urlpatterns = [
    path('', views.maintenance_form, name='request'),
]