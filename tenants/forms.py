from django import forms
from properties.models import InvitationCode, Tenant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div, Submit
from django.contrib.auth import get_user_model

class InvitationCodeForm(forms.ModelForm):
    tenant_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    apartment = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Apt. #'}))
    rent_amount = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Amount'}))
    next_rent_due = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    lease_end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = InvitationCode
        fields = ['tenant_name', 'property', 'apartment', 'rent_amount', 'next_rent_due', 'lease_end']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['property'].queryset = user.properties.all()
        


        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'invitation-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('tenant_name', css_class='form-control', title="Tenant Name"),
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
                    Field('next_rent_due', css_class='form-control', title="First Rent Due"),
                    css_class='col',
                ),
            ),
            Field('lease_end', css_class='form-control'),
            Submit('form1', 'Save', css_class='btn btn-primary col-12 mt-1'),
        )

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
        css = {"all": ["form-control form-control-user"]}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'profile-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('first_name', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('last_name', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Field('email', css_class='form-control'),
            Field('phone_number', css_class='form-control'),
            Field('profile_image', css_class='form-control-file'),
            Submit('form1', 'Save', css_class='btn btn-primary col-12 mt-1'),
        )

class EditTenantForm(forms.ModelForm):
    next_rent_due = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    lease_end = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Tenant
        fields = ['apartment', 'rent_amount', 'next_rent_due', 'lease_end', 'is_active', 'outstanding_rent', 'overdue_fee']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'tenant-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('is_active', css_class='form-control'),
            Row(
                Div(
                    Field('rent_amount', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('next_rent_due', css_class='form-control', title="First Rent Due"),
                    css_class='col',
                ),
            ),
            Row(
                Div(
                    Field('outstanding_rent', css_class='form-control'),
                    css_class='col',
                    ),
                Div(
                    Field('overdue_fee', css_class='form-control'),
                    css_class='col',
                    ),
            ),
            Row(
                Div(
                    Field('apartment', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('lease_end', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Div(
                Submit('tenant_form', 'Save', css_class='btn btn-primary col-12 mt-1'),
                css_class='modal-footer',
            ),
        )