import django_tables2 as tables
from .models import Tenant

class CustomTenantTable(tables.Table):
    full_name = tables.Column(verbose_name='Full Name', accessor='resident', order_by=('resident__first_name', 'resident__last_name'))
    change = tables.TemplateColumn("<a class='text-dark profile-btn' href='{% url 'user_profile' user_id=record.resident.user_id %}'><i class='fa fa-cog'></i></a>", verbose_name='')

    class Meta:
        model = Tenant
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        fields = ("full_name", "apartment", "change")

    def render_full_name(self, record):
        return f"{record.resident.first_name} {record.resident.last_name}"
