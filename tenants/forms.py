from django import forms
from properties.models import InvitationCode

class InvitationCodeForm(forms.ModelForm):
    class Meta:
        model = InvitationCode
        fields = ['property', 'rent_amount', 'lease_end', 'next_rent_due', 'apartment']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['property'].queryset = user.properties.all()
