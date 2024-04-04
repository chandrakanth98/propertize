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


        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'property-notice-form'
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('body', css_class='form-control', rows="4"),
            Row(
                Div(
                    Field('property', css_class='form-control'),
                    css_class='col',
                ),
                Div(
                    Field('posted_by', css_class='form-control'),
                    css_class='col',
                ),
            ),
            Field('important', css_class='form-check-input'),
            Submit('form1', 'Post', css_class='btn btn-primary col-12 mt-1'),
        )

class EditProperty(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'zip_code', 'city', 'details', 'featured_image']
        css = {"all": ["form-control form-control-user"]}
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

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
                Div(
                HTML('<button type="button" class="btn btn-danger ml-2" data-toggle="modal" data-dismiss="modal" data-target="#deleteModal">Delete</button>'),
                ),
                Div(
                HTML('<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'),
                Submit('form2', 'Save', css_class='btn btn-primary ml-2'),
                ),
            css_class="modal-footer d-flex justify-content-between align-items-center row"
            ), 
        )

class addProperty(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['landlord', 'name', 'address', 'zip_code', 'city', 'details', 'featured_image']
    
    def __init__(self, *args, landlord=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['landlord'].initial = landlord

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'add-property-form'
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
                Submit('submit', 'Save', css_class='btn btn-primary ml-2'),
            ),
            css_class="modal-footer"
            ), 
        )
