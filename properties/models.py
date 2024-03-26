from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

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
    

class InvitationCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='invitation_code')

    def __str__(self):
        return str(self.code)

@receiver(post_save, sender=Property)
def create_invitation_code(sender, instance, created, **kwargs):
    if created:
        InvitationCode.objects.create(property=instance)