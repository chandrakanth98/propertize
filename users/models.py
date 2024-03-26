from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = ((0, 'None'), (1, 'Landlord'), (2, 'Contractor'), (3, 'Tenant'))

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True, unique=True)
    role = models.IntegerField(choices=ROLE, default=0)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    assigned_property = models.ForeignKey('properties.Property', on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name='tenants')

    def __str__(self):
            return self.username