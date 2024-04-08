from datetime import datetime, timedelta

from django.urls import reverse
from django.test import TestCase
from tenants.models import Tenant
from maintenance.models import Worker
from properties.models import Property
from properties.models import InvitationCode
from django.contrib.auth import get_user_model

User = get_user_model()

class InvitationFormTest(TestCase):
    def setUp(self):

        self.landlord = User.objects.create_user(username='landlord', password='testpass123', role=1)

        self.property = Property.objects.create(landlord=self.landlord, address='420 Test St', zip_code=1337, city='Test City', name='Test Property')

        self.tenant_user = User.objects.create_user(username='tenant', password='testpass123', role=3)

        self.tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date(),
            apartment='1A',
            is_active=True
        )

        self.none_user = User.objects.create_user(username='none', password='testpass123', role=0)

        self.invitation_code = InvitationCode.objects.create(
            used=False,
            property=self.property,
            rent_amount=1000,
            lease_end='2025-04-30',
            next_rent_due='2024-04-30',
            apartment='testapartment',
            tenant_name='testtenantname',
        )
        self.worker_code = Worker.objects.create(
            used=False,
            code_name='testworkername',
        )
        self.worker_code.assigned_properties.set([self.property])

    def test_tenant_invitation_form_submission(self):
        self.client.login(username='none', password='testpass123')
        self.assertTrue(self.none_user.role == 0)

        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('invite'))
        response = self.client.post(reverse(
            'invite'), {'invitation_code': self.invitation_code.code}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.none_user.refresh_from_db()
        self.assertTrue(self.none_user.role == 3)
        self.assertTrue(self.none_user.assigned_property, self.property)
        self.assertTrue(Tenant.objects.filter(resident=self.none_user).exists())
        self.assertTrue(InvitationCode.objects.get(code=self.invitation_code.code).used)

    def test_worker_invitation_form_submission(self):
        self.client.login(username='none', password='testpass123')
        self.assertTrue(self.none_user.role == 0)

        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('invite'))
        response = self.client.post(reverse(
            'invite'), {'invitation_code': self.worker_code.code}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.none_user.refresh_from_db()
        self.assertTrue(self.none_user.role == 2)
        self.assertTrue(self.property.assigned_contractor.filter(
            user_id=self.none_user.user_id).exists())
        self.assertTrue(Worker.objects.get(code=self.worker_code.code).used)

    def test_tenant_invitation_form_submission_invalid_code(self):
        self.client.login(username='none', password='testpass123')
        self.assertTrue(self.none_user.role == 0)

        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('invite'))
        response = self.client.post(reverse(
            'invite'), {'invitation_code': 'invalidcode'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid invitation code')
        self.none_user.refresh_from_db()
        self.assertTrue(self.none_user.role == 0)
