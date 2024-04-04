import django_tables2 as tables
from .models import Tenant
from properties.models import InvitationCode

class TenantTable(tables.Table):
    full_name = tables.Column(verbose_name='Full Name', accessor='resident', order_by=('resident__first_name', 'resident__last_name'))
    change = tables.TemplateColumn("<a class='text-dark profile-btn' href='{% url 'user_profile' user_id=record.resident.user_id %}'><i class='fa fa-cog'></i></a>", verbose_name='')

    class Meta:
        model = Tenant
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        sequence = ("change", "full_name", "apartment", "rent_amount", "outstanding_rent", "lease_end")
        exclude = ("tenant_id", "resident", "is_active", "current_rent_period_start", "current_rent_period_end", "overdue_fee", "next_rent_due",)

    def render_full_name(self, record):
        return f"{record.resident.first_name} {record.resident.last_name}"
    
class InvitationCodeTable(tables.Table):
    property_name = tables.Column(verbose_name='Property', accessor='property.name')

    class Meta:
        model = InvitationCode
        orderable = True
        attrs = {"class": "table table-hover"}
        fields = ("code", "used", "property_name", "tenant_name", "apartment")
