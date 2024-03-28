from django import forms
from properties.models import InvitationCode

class InvitationCodeForm(forms.ModelForm):
    class Meta:
        model = InvitationCode
        fields = ['tenant_name', 'property', 'apartment', 'rent_amount', 'next_rent_due', 'lease_end']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['property'].queryset = user.properties.all()
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})