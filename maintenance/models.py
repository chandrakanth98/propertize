from django.db import models
from properties.models import Property
from django.contrib.auth import get_user_model

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
    description = models.TextField(max_length=280)
    urgent = models.IntegerField(choices=URGENT, default=0)
    contractor_note = models.TextField(max_length=280)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    location = models.CharField(max_length=120, default="Unknown")

    def __str__(self):
                return f"Request from: {self.submitted_by.first_name} {self.submitted_by.last_name} at {self.property.name}"