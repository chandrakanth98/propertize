import django_tables2 as tables
from .models import Tenant

class TenantTable(tables.Table):
    full_name = tables.Column(verbose_name='Full Name', accessor='resident', order_by=('resident__first_name', 'resident__last_name'))

    class Meta:
        model = Tenant
        attrs = {"class": "table table-bordered",}
        sequence = ("full_name", "outstanding_rent", "rent_amount", "next_rent_due", "apartment", "lease_end")
        exclude = ("tenant_id", "resident")

    def render_full_name(self, record):
        return f"{record.resident.first_name} {record.resident.last_name}"

        
