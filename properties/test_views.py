from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property


class TestPropertiesViews(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user_landlord = User.objects.create_superuser(
            username="landlordUser",
            password="landlordPassword",
            email="landlord@test.com",
            first_name='Landlord',
            last_name='User',
            role=1
        )

        self.property1 = Property(landlord=self.user_landlord, address="Testington 1",
                                 zip_code="42069", city='Velo', name="Velo apt test")
        
        self.property2 = Property(landlord=self.user_landlord, address="Testington 2",
                                 zip_code="69420", city='Velo', name="Schweppes")
        self.property1.save()
        self.property2.save()

    def test_render_landlords_properties(self):
        """ Test that properties renders the logged in users properties """
        self.client.login(
            username="landlordUser", password="landlordPassword")
        response = self.client.get(reverse('properties'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Velo apt test", response.content)
        self.assertIn(b"Schweppes", response.content)
        self.assertIn(b"Testington 1", response.content)