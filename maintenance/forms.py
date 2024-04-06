from django import forms
from django.forms import CheckboxSelectMultiple
from .models import MaintenanceRequest, Worker
from properties.models import Property
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row

class MaintenanceForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apt, staircase, etc.'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please describe the issue in detail so the contractor can come prepared.'}))
    class Meta:
        model = MaintenanceRequest
        fields = ['description', 'property', 'location', 'urgent']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['property'].queryset = Property.objects.filter(tenants=user)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'maintenance-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('property', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('location', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Field('description', css_class='form-control', rows=5),
            Field('urgent', css_class='form-control'),
            Submit('form', 'Save', css_class='btn btn-primary col-12 mt-1'),
        )

class EditMaintenanceForm(forms.ModelForm):
    STATUS = ((0, 'Submitted'), (3, 'Cancel'))
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}),)
    class Meta:
        model = MaintenanceRequest
        fields = ['description', 'location', 'urgent', 'status']
        css = {"all": ["form-control form-control-user"]}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'maintenance-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('description', css_class='form-control', rows=5),
            Field('location', css_class='form-control'),
            Row(
                Div(
                    Field('urgent', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('status', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Submit('form', 'Save', css_class='btn btn-primary col-12 mt-1'),
        )


class WorkerCodeForm(forms.ModelForm):
    assigned_properties = forms.ModelMultipleChoiceField(
        queryset=Property.objects.all(), 
        widget=CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Worker
        fields = ['code_name', 'assigned_properties']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user is not None:
            self.fields['assigned_properties'].queryset = Property.objects.filter(landlord=user)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'worker-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('code_name', css_class='form-control'),
            Field('assigned_properties', css_class='form-control'),
            Submit('form', 'Save', css_class='btn btn-primary col-12 mt-1'),
        )
