from django.contrib import admin
from .models import MaintenanceRequest, Worker

# Register your models here.

admin.site.register(MaintenanceRequest)
admin.site.register(Worker)