from django import forms
from properties.models import InvitationCode
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div, Submit

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

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'invitation-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('tenant_name', css_class='form-control', placeholder='Tenant Name', value=None),
            Row(
                Div(
                    Field('property', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('apartment', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Row(
                Div(
                    Field('rent_amount', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('next_rent_due', css_class='form-control', attrs={'data-provide': 'datepicker'}),
                    css_class='col',
                ),
            ),
            Field('lease_end', css_class='form-control'),
            Submit('submit', 'Invite', css_class='btn btn-primary col-12 mt-1'),
        )