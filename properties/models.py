from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Property(models.Model):
    property_id = models.AutoField(unique=True, primary_key=True)
    landlord = models.ForeignKey(User, on_delete=models.PROTECT, related_name="properties")
    address = models.CharField(max_length=150)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    def __str__(self):
            return self.name
