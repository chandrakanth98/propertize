from allauth.account.forms import SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div, Submit

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(max_length=15, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'signup-form'
        self.helper.form_action = 'account_signup'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Row(
                Div(
                    Field('first_name', css_class='form-control', placeholder='First Name'),
                    css_class='col',
                ),
                Div(
                    Field('last_name', css_class='form-control', placeholder='Last Name'),
                    css_class='col',
                ),
            ),
            Row(
                Div(
                    Field('phone_number', css_class='form-control', placeholder='Phone Number'),
                    css_class='col',
                ),
                Div(
                    Field('email', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Row(
                Div(
                    Field('password1', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('password2', css_class='form-control'),
                    css_class='col',
                    ),
            ),
            Submit('submit', 'Sign Up', css_class='btn btn-primary col-12 mt-1'),
        )
    
    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
