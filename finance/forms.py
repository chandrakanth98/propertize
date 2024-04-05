from django import forms
from finance.models import Transaction
from crispy_forms.helper import FormHelper
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