from calendar import monthrange
from datetime import datetime, timedelta

from django.test import TestCase
from tenants.models import Tenant
from finance.models import Transaction
from properties.models import Property
from django.contrib.auth import get_user_model
from finance.tasks import generate_rent_invoices
from dateutil.relativedelta import relativedelta

User = get_user_model()

class GenerateRentInvoicesTest(TestCase):
    """
    A test case for generating rent invoices.

    This test case sets up the necessary data for generating rent invoices and then verifies that the invoices are generated correctly.
    """

    def setUp(self):
        # landlord user
        self.landlord = User.objects.create_user(username='landlord', password='testpass123', role=1)

        # property
        self.property = Property.objects.create(landlord=self.landlord, address='420 Test St', zip_code=1337, city='Test City', name='Test Property')

        # tenant user
        self.tenant_user = User.objects.create_user(username='tenant', password='testpass123', role=3, assigned_property=self.property)

        # tenant model
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

    def test_generate_rent_invoices(self):
        """
        Test case for generating rent invoices.

        This test case verifies that the `generate_rent_invoices` function correctly generates rent invoices
        and updates the necessary fields in the `Tenant` and `Transaction` models.

        """
        generate_rent_invoices()
        tenant = Tenant.objects.get(tenant_id=self.tenant.tenant_id)
        self.assertIsNotNone(tenant.current_rent_period_start)
        self.assertIsNotNone(tenant.current_rent_period_end)
        next_month = datetime.now().date().replace(month=datetime.now().date().month + 1)
        next_month_end = next_month.replace(day=monthrange(next_month.year, next_month.month)[1])
        self.assertEqual(tenant.next_rent_due, next_month_end)
        transaction = Transaction.objects.filter(user=tenant.resident, transaction_month=tenant.current_rent_period_start)
        self.assertTrue(transaction.exists())
        self.assertEqual(transaction.first().amount, tenant.rent_amount + tenant.outstanding_rent)

    def test_inactive_tenant(self):
        """
        Test case to verify that no transaction is created for an inactive tenant.
        """
        self.tenant.delete()
        inactive_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date(),
            apartment='1B',
            is_active=False
        )
        generate_rent_invoices()
        self.assertFalse(Transaction.objects.filter(user=inactive_tenant.resident).exists())

    def test_future_rent_due(self):
        """
        Test case to verify that no transaction is created for a tenant with next rent due in a future month.
        """
        self.tenant.delete()
        future_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date() + relativedelta(months=2),
            apartment='1C',
            is_active=True
        )
        generate_rent_invoices()
        self.assertFalse(Transaction.objects.filter(user=future_tenant.resident).exists())

    def test_unpaid_transactions(self):
        """
        Test case for handling unpaid transactions.

        This test case verifies that when a tenant has unpaid transactions from 
        the previous month, the 'generate_rent_invoices' function 
        correctly updates the tenant's outstanding rent and creates 
        a new invoice for the tenant.

        """
        self.tenant.delete()
        unpaid_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=0,
            next_rent_due=datetime.now().date(),
            apartment='1D',
            is_active=True
        )
        Transaction.objects.create(
            user=unpaid_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=500,
            type=1,
            note='Rent invoice for',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=30)
        )
        generate_rent_invoices()
        unpaid_tenant.refresh_from_db()
        self.assertEqual(unpaid_tenant.outstanding_rent, 0)
        self.assertTrue(Transaction.objects.filter(user=unpaid_tenant.resident, status=2).exists())
        new_invoice = Transaction.objects.filter(user=unpaid_tenant.resident, transaction_month=datetime.now().date().replace(day=1)).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, unpaid_tenant.rent_amount + 500)

    def test_existing_transaction(self):
        """
        Test case to verify that no new transaction is created when an existing transaction already exists.
        """
        self.tenant.delete()  
        current_month_name = datetime.now().date().strftime("%B")
        existing_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date(),
            apartment='1E',
            is_active=True
        )
        Transaction.objects.create(
            user=existing_tenant.resident,
            due_date=datetime.now().date(),
            status=0,
            amount=1000,
            type=1,
            note='Rent invoice for ' + current_month_name,
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1)
        )
        generate_rent_invoices()
        self.assertEqual(Transaction.objects.filter(user=existing_tenant.resident).count(), 1)

    def test_multiple_unpaid_transactions(self):
        """
        Test case to verify the behavior of generating rent invoices for a tenant with multiple unpaid transactions.
        """
        self.tenant.delete()
        unpaid_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=0,
            next_rent_due=datetime.now().date(),
            apartment='1F',
            is_active=True
        )
        Transaction.objects.create(
            user=unpaid_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=500,
            type=1,
            note='Rent invoice for',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=60)
        )
        Transaction.objects.create(
            user=unpaid_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=300,
            type=1,
            note='Rent invoice for',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=30)
        )
        generate_rent_invoices()
        unpaid_tenant.refresh_from_db()
        self.assertEqual(unpaid_tenant.outstanding_rent, 0)
        self.assertTrue(Transaction.objects.filter(user=unpaid_tenant.resident, status=2).exists())
        new_invoice = Transaction.objects.filter(user=unpaid_tenant.resident, transaction_month=datetime.now().date().replace(day=1)).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, unpaid_tenant.rent_amount + 800)

    def test_tenant_with_overdue_fee(self):
        """
        Test case to verify the generation of rent invoices for a tenant with an overdue fee.
        """
        self.tenant.delete()
        overdue_fee_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=100,
            next_rent_due=datetime.now().date(),
            apartment='1H',
            is_active=True
        )
        generate_rent_invoices()
        new_invoice = Transaction.objects.filter(user=overdue_fee_tenant.resident, transaction_month=datetime.now().date().replace(day=1)).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, overdue_fee_tenant.rent_amount)
        expected_amount = overdue_fee_tenant.rent_amount + overdue_fee_tenant.outstanding_rent
        self.assertEqual(new_invoice.amount, expected_amount)

    def test_tenant_with_zero_rent(self):
        """
        Test case to verify the behavior when a tenant has zero rent amount.
        """
        self.tenant.delete()
        zero_rent_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=0,
            outstanding_rent=0,
            overdue_fee=0,
            next_rent_due=datetime.now().date(),
            apartment='1J',
            is_active=True
        )
        generate_rent_invoices()
        new_invoice = Transaction.objects.filter(user=zero_rent_tenant.resident, transaction_month=datetime.now().date().replace(day=1)).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, 0)

    def test_tenant_with_negative_rent(self):
        self.tenant.delete()
        negative_rent_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=-1000,
            outstanding_rent=0,
            overdue_fee=0,
            next_rent_due=datetime.now().date(),
            apartment='1K',
            is_active=True
        )
        generate_rent_invoices()
        new_invoice = Transaction.objects.filter(user=negative_rent_tenant.resident, transaction_month=datetime.now().date().replace(day=1)).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, 0)

    def test_past_rent_due_date(self):
        self.tenant.delete()
        past_due_date_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date() - relativedelta(months=1),
            apartment='1L',
            is_active=True
        )
        generate_rent_invoices()
        self.assertTrue(Transaction.objects.filter(user=past_due_date_tenant.resident).exists())

    def test_unpaid_not_overdue(self):
        """
        Test case to verify the behavior when a tenant has an unpaid transaction
        but it is not overdue.
        """
        self.tenant.delete()
        unpaid_not_overdue_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            overdue_fee_days=99,
            next_rent_due=datetime.now().date(),
            apartment='1M',
            is_active=True
        )
        Transaction.objects.create(
            user=unpaid_not_overdue_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=1000,
            type=1,
            note='Rent invoice for',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=30)
        )
        generate_rent_invoices()
        self.assertTrue(Transaction.objects.filter(user=unpaid_not_overdue_tenant.resident, status=0).exists())
        self.assertEqual(unpaid_not_overdue_tenant.outstanding_rent, 0)

    def test_overdue_fee_days(self):
        """
        Test case to verify the behavior when a tenant has an overdue fee
        and the overdue fee days are greater than the overdue days.
        """
        self.tenant.delete()
        overdue_fee_days_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            overdue_fee_days=1,
            next_rent_due=datetime.now().date(),
            apartment='1N',
            is_active=True
        )
        Transaction.objects.create(
            user=overdue_fee_days_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=1000,
            type=1,
            note='Rent invoice for',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=30)
        )
        generate_rent_invoices()
        self.assertTrue(Transaction.objects.filter(user=overdue_fee_days_tenant.resident, status=2).exists())
        self.assertEqual(overdue_fee_days_tenant.outstanding_rent, 0)
        new_invoice = Transaction.objects.filter(user=overdue_fee_days_tenant.resident, status=0).first()
        self.assertIsNotNone(new_invoice)
        self.assertEqual(new_invoice.amount, 1000 + overdue_fee_days_tenant.rent_amount + overdue_fee_days_tenant.overdue_fee)
        self.assertTrue('Outstanding Balance' in new_invoice.note)

    def test_startswith_condition(self):
        """
        Test case to verify the behavior when a tenant has an unpaid transaction
        with a note that does not start with 'Rent invoice for'.
        """
        self.tenant.delete()
        startswith_tenant = Tenant.objects.create(
            resident=self.tenant_user,
            lease_end=datetime.now().date() + timedelta(days=365),
            rent_amount=1000,
            outstanding_rent=0,
            overdue_fee=50,
            next_rent_due=datetime.now().date(),
            apartment='1O',
            is_active=True
        )
        Transaction.objects.create(
            user=startswith_tenant.resident,
            due_date=datetime.now().date() - timedelta(days=30),
            status=0,
            amount=1000,
            type=1,
            note='Unpaid transaction',
            property=self.property,
            overdue_fee=0,
            transaction_month=datetime.now().date().replace(day=1) - timedelta(days=30)
        )
        generate_rent_invoices()
        transactions = Transaction.objects.filter(user=startswith_tenant.resident)
        self.assertEqual(transactions.count(), 2)
        self.assertEqual(transactions.filter(note__startswith="Rent invoice for").count(), 1)
        self.assertEqual(transactions.filter(note__startswith="Rent invoice for", amount=1000).count(), 1)
        self.assertEqual(transactions.filter(note='Unpaid transaction').count(), 1)
        self.assertEqual(transactions.filter(note='Unpaid transaction', amount=1000).count(), 1)
