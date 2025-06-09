from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE = (
    (0, 'None'),
    (1, 'Landlord'),
    (2, 'Contractor'),
    (3, 'Tenant'),
)

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True, unique=True)
    role = models.IntegerField(choices=ROLE, default=0)

    # You already inherited first_name/last_name on AbstractUser,
    # but if you want to enforce non-null:
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    assigned_property = models.ForeignKey(
        'properties.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tenants'
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default='',  # empty string means “no image uploaded”
        help_text="Leave blank to use the default avatar."
    )

    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
