from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import Container, InnerContainer
from .choices import CONTANER_NAMES, EXTRA_FILTER_OPTIONS


class ContainerForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = '__all__'


class InnerContainerForm(forms.ModelForm):

    class Meta:
        model = InnerContainer
        fields = '__all__'


class ContainerSelectionForm(forms.Form):

    container_name = forms.ChoiceField(
        choices=CONTANER_NAMES, required=True, label='Container Name')

    def __init__(self, *args, **kwargs):
        super(ContainerSelectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            'container_name',  # field1 will appear first in HTML
            Submit('submit', u'Submit', css_class="btn btn-sm btn-default"),
        )


class CreateContainerForm(forms.Form):

    extra_filter_field_attr = forms.ChoiceField(
        choices=EXTRA_FILTER_OPTIONS, required=True, label='Extra filter field attribute')

    def __init__(self, *args, **kwargs):
        super(CreateContainerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            'extra_filter_field_attr',  # field1 will appear first in HTML
            Submit('submit', u'Submit', css_class="btn btn-sm btn-default"),
        )
