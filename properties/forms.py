from django import forms
from properties.models import PropertyNotice, Property
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Div, Submit, HTML

class PropertyNoticeForm(forms.ModelForm):
    
    class Meta:
        model = PropertyNotice
        fields = ['title', 'body', 'property', 'posted_by', 'important']
        css = {"all": ["form-control form-control-user"]}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['property'].queryset = user.properties.all()
            property = forms.ChoiceField(choices=[(property.property_id, property.name) for property in user.properties.all()])
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class EditProperty(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'zip_code', 'city', 'details', 'featured_image']
        css = {"all": ["form-control form-control-user"]}
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'edit-property-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Row(
                Div(
                    Field('address', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('zip_code', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('city', css_class='form-control'),
                    css_class='col',
                ),
            ),

            Field('details', css_class='form-control', rows="3"),
            Field('featured_image', css_class='form-control-file'),
            Div(
                Row(
                    HTML('<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'),
                    Submit('form2', 'Save', css_class='btn btn-primary ml-2'),
                ),
                css_class="modal-footer"
            ), 
        )