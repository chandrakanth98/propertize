import django_tables2 as tables

from .models import Tenant
from properties.models import InvitationCode


class TenantTable(tables.Table):
    full_name = tables.Column(verbose_name='Full Name', accessor='resident', order_by=('resident__first_name', 'resident__last_name'))
    change = tables.TemplateColumn("<a class='text-dark profile-btn' href='{% url 'user_profile' user_id=record.resident.user_id %}'><i class='fa fa-cog'></i></a>", verbose_name='')
    is_active = tables.BooleanColumn(verbose_name='Active', accessor='is_active')
    property = tables.Column(verbose_name='Property', accessor='resident.assigned_property.name')
    user_id = tables.Column(verbose_name='User ID', accessor='resident.user_id')
    outstanding_rent = tables.Column(verbose_name='Outstanding')

    class Meta:
        model = Tenant
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        sequence = ("is_active", "user_id", "full_name", "property", "apartment", "outstanding_rent", "lease_end", "change")
        exclude = ("tenant_id", "resident", "current_rent_period_start", "current_rent_period_end", "overdue_fee", "next_rent_due", "rent_amount", "overdue_fee_days", "overdue")

    def render_full_name(self, record):
        return f"{record.resident.first_name} {record.resident.last_name}"

class InvitationCodeTable(tables.Table):
    property_name = tables.Column(verbose_name='Property', accessor='property.name')
    delete = tables.TemplateColumn(template_code='''
        <a class="text-danger delete-link" style="cursor:pointer;" data-toggle="modal" data-target="#deleteInvitation" data-url="{% url 'delete_invitation' code_id=record.id %}" data-code="{{ record.code }}">
    <i class="fa fa-trash"></i>
</a>''', verbose_name='')
    class Meta:
        model = InvitationCode
        orderable = True
        attrs = {"class": "table table-hover"}
        fields = ("code", "used", "property_name", "tenant_name", "apartment")
