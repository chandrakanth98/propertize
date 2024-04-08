import django_filters

from decimal import Decimal

from tenants.models import Tenant
from django.db.models import Q, Value
from properties.models import InvitationCode
from django.db.models.functions import Concat


class TenantFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', label='Search',)

    class Meta:
        model = Tenant
        fields = ['query']

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return Tenant.objects.filter(
                Q(rent_amount=value) | Q(outstanding_rent=value)
            )

        return Tenant.objects.annotate(
            full_name=Concat('resident__first_name', Value(' '), 'resident__last_name')
            ).filter(
            Q(resident__first_name__icontains=value) |
              Q(resident__last_name__icontains=value) | Q(apartment__icontains=value) | Q(full_name__icontains=value)
              | Q(resident__assigned_property__name__icontains=value)
        )


class InvitationCodeFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', label='Search',)

    class Meta:
        model = InvitationCode
        fields = ['query']

    def universal_search(self, queryset, name, value):

        return InvitationCode.objects.filter(
            Q(code__icontains=value) |
              Q(property__name__icontains=value) | Q(apartment__icontains=value) |
                Q(tenant_name__icontains=value) | Q(used__icontains=value)
        )