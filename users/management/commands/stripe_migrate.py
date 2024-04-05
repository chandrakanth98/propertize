from django.core.management.base import BaseCommand
from djstripe.models import Customer as DjstripeCustomer
from users.models import CustomUser
import stripe

class Command(BaseCommand):
    help = 'Create Stripe customers for existing users'

    def handle(self, *args, **options):
        users_without_stripe_customer = CustomUser.objects.filter(stripe_customer__isnull=True)
        for user in users_without_stripe_customer:
            # Create a customer in Stripe
            stripe_customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}",
            )

            # Create a Customer object in the database
            djstripe_customer = DjstripeCustomer.objects.create(
                subscriber=user,
                stripe_id=stripe_customer.id,
                default_currency=stripe_customer.currency,
                livemode=stripe_customer.livemode,
                name=stripe_customer.name,
                email=stripe_customer.email,
            )

            user.stripe_customer = djstripe_customer
            user.save()