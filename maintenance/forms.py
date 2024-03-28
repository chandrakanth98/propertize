from django import forms
from .models import MaintenanceRequest
from properties.models import Property

class MaintenanceForm(forms.ModelForm):
    
    class Meta:
        model = MaintenanceRequest
        fields = ['description', 'property', 'urgent']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['property'].queryset = Property.objects.filter(tenants=user)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})