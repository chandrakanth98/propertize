import django_tables2 as tables

from properties.models import Property
from .models import MaintenanceRequest, Worker
from django.contrib.auth import get_user_model


class MaintenanceRequestTable(tables.Table):
    property_name = tables.Column(verbose_name='Property', accessor='property.name')
    full_name = tables.Column(verbose_name='Full Name', accessor='submitted_by', order_by=('submitted_by__first_name', 'submitted_by__last_name'))
    contractor = tables.Column(verbose_name='Contractor', accessor='contractor.first_name')
    location = tables.Column(verbose_name='Location')
    open = tables.TemplateColumn("<a class='text-dark profile-btn' href='{% url 'maintenance_request' request_id=record.request_id %}'><i class='fa fa-cog'></i></a>", verbose_name='')

    class Meta:
        model = MaintenanceRequest
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        fields = ("open", "status", "property_name", "full_name", "contractor", "request_date", "location")
    
    def render_full_name(self, record):
        return f"{record.submitted_by.first_name} {record.submitted_by.last_name}"
    
class WorkerCodeTable(tables.Table):
    delete = tables.TemplateColumn(template_code='''
        <a class="text-danger delete-link" style="cursor:pointer;" data-toggle="modal" data-target="#deleteInvitation" data-url="{% url 'delete_invitation_contractor' code_id=record.id %}" data-code="{{ record.code }}">
    <i class="fa fa-trash"></i>
</a>''', verbose_name='')
    
    def render_code_name(self, value):
        return value if len(value) <= 8 else value[:8] + '...'


    class Meta:
        model = Worker
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        fields = ("code", "used", "code_name", "assigned_properties", "delete")


class ContractorTable(tables.Table):
    first_name = tables.Column(verbose_name='First Name', accessor='first_name')
    last_name = tables.Column(verbose_name='Last Name', accessor='last_name')
    change = tables.TemplateColumn("<a class='text-dark profile-btn' href='{% url 'user_profile' user_id=record.pk %}'><i class='fa fa-cog'></i></a>", verbose_name='')
    
    


    class Meta:
        model = Property
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        fields = ("change","role", "first_name", "last_name", "email", "phone_number", "assigned_contractor",)


