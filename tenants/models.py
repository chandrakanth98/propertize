from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Tenant(models.Model):
    tenant_id = models.AutoField(unique=True, primary_key=True)
    renter = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tenant")
    lease_end = models.DateField()
    rent_amount = models.FloatField()
    next_rent_due = models.DateField()

    def __str__(self):
            return self.renter.username

