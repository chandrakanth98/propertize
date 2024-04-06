from django.db import models
from properties.models import Property
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()
# Create your models here.

URGENT = ((0, 'No'), (1, 'Yes'))
STATUS = ((0, 'Submitted'), (1, 'In-progress'), (2, 'Completed'), (3, 'Cancelled'))

class MaintenanceRequest(models.Model):
    request_id = models.AutoField(unique=True, primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE,
                                  related_name="maintenance_property")
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="submitted_by")
    contractor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="contractor",
                                    limit_choices_to= {'role': 2}, default=None)
    description = models.TextField()
    urgent = models.IntegerField(choices=URGENT, default=0)
    contractor_note = models.TextField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    location = models.CharField(max_length=120, default="Unknown")

    def __str__(self):
                return f"Request from: {self.submitted_by.first_name} {self.submitted_by.last_name} at {self.property.name}"
    

class Worker(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    code_name = models.CharField(max_length=120)
    assigned_properties = models.ManyToManyField(Property, related_name="assigned_properties")
    contractor = models.BooleanField(default=True)
    code = models.CharField(max_length=5, unique=True, blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Worker: {self.code}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        return str(uuid.uuid4().hex)[:5]