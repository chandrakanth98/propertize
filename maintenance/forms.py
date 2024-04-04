from django import forms
from .models import MaintenanceRequest
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