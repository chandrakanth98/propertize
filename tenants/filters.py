from decimal import Decimal
from django.db.models import Q
import django_filters
from tenants.models import Tenant


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

        return Tenant.objects.filter(
            Q(resident__first_name__icontains=value) |
              Q(resident__last_name__icontains=value) | Q(apartment__icontains=value)
        )