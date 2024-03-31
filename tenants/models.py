from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Tenant(models.Model):
    tenant_id = models.AutoField(unique=True, primary_key=True)
    resident = models.ForeignKey(User, on_delete=models.PROTECT, related_name="resident")
    lease_end = models.DateField()
    rent_amount = models.FloatField()
    outstanding_rent = models.FloatField(default=0)
    overdue_fee = models.FloatField(default=0)
    next_rent_due = models.DateField()
    apartment = models.CharField(default=0, max_length=50)
    is_active = models.BooleanField(default=True)
    current_rent_period_start = models.DateField(null=True, blank=True)
    current_rent_period_end = models.DateField(null=True, blank=True)

    def __str__(self):
            return(f"{self.resident.last_name}, {self.resident.first_name}, {self.resident.assigned_property.name}")

