from decimal import Decimal
from django.db.models import Q, Value
from django.db.models.functions import Concat
import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', label='Search',
    )
    status = django_filters.CharFilter(
        field_name='status', lookup_expr='icontains'
    )
    type = django_filters.CharFilter(
        field_name='type', lookup_expr='icontains'
    )
    class Meta:
        model = Transaction
        fields = ['query']

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return Transaction.objects.filter(
                Q(created_on=value) | Q(due_date=value) | Q(amount=value) 
            )

        return Transaction.objects.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        ).filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) | Q(type__icontains=value) |
            Q(status__icontains=value) | Q(full_name__icontains=value) 
        )