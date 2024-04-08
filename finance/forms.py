from django import forms

from tenants.models import Tenant
from finance.models import Transaction
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from crispy_forms.layout import Layout, Field, Row, Div, Submit, HTML


class EditTransactionForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})),
    class Meta:
        model = Transaction
        fields = ['status', 'due_date', 'amount', 'type']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'edit-transaction-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('status', css_class='form-control'),
            Field('due_date', css_class='form-control'),
            Field('amount', css_class='form-control'),
            Field('type', css_class='form-control'),
            Row(
                Div(
                HTML('<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'),
                css_class='col',
                ),
                Div(
                    Submit('form', 'Save', css_class='btn btn-primary col-12 mt-1'),
                    css_class='col',
                ),
                css_class='modal-footer',
            ),
        )

class CreateTransactionForm(forms.ModelForm):
    User = get_user_model()
    status = forms.ChoiceField(initial=0, required=False)
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    user = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.NumberInput(attrs={'placeholder': 'User ID'}), empty_label=None, required=False, help_text="Enter the User ID if you are creating an invoice for someone else to pay. Leave empty to link it to your account.")

    class Meta:
        model = Transaction
        fields = ['status', 'due_date', 'amount', 'type', 'property', 'user', 'note']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, user=None, tenants=None, properties=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenants is not None:
            self.fields['user'].queryset = tenants
        if properties is not None:
            self.fields['property'].queryset = properties

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'create-transaction-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Row(
            Div(
                Field('type', css_class='form-control'),
                css_class="col"
            ),
            Div(
                Field('property', css_class='form-control'),
                css_class="col"
            ),
            ),
            Row(
                Div(
                    Field('user', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('amount', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Field('due_date', css_class='form-control'),
            Field('note', css_class='form-control'),
            Submit('form', 'Create', css_class='btn btn-primary col-12 mt-1')

            )
