import django_filters

from decimal import Decimal

from django.db.models import Q, Value
from properties.models import Property
from django.db.models.functions import Concat
from .models import MaintenanceRequest, Worker
from django.contrib.auth import get_user_model


class MaintenanceFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', label='Search',)
    status = django_filters.CharFilter(
        field_name='status', lookup_expr='icontains'
    )

    class Meta:
        model = MaintenanceRequest
        fields = ['query']

    def universal_search(self, queryset, name, value):

        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return MaintenanceRequest.objects.filter(
                Q(request_id=value) | Q(request_date=value)
            )

        return MaintenanceRequest.objects.annotate(
            full_name=Concat('submitted_by__first_name', Value(' '), 'submitted_by__last_name')
            ).filter(
                Q(submitted_by__first_name__icontains=value) |
                Q(submitted_by__last_name__icontains=value) | Q(property__name__icontains=value) |
                Q(location__icontains=value) | Q(status__icontains=value) | Q(full_name__icontains=value)
            )


class WorkerFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', label='Search',)

    class Meta:
        model = Worker
        fields = ['query']


class ContractorFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label='Search',)
    
    class Meta:
        User = get_user_model()
        model = User
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone_number__icontains=value) |
            Q(assigned_contractor__name__icontains=value)
        )
