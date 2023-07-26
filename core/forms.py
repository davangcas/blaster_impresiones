from crispy_forms.helper import FormHelper
from django import forms
from django.forms.fields import DateField, TimeField

from core.fields import CommonLayout, CustomDateField, CustomTimeField


class DefaultModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-3 col-form-label text-right"
        self.helper.field_class = "col-sm-8"

        fields = []
        for field_name, field in self.fields.items():
            if isinstance(field, DateField):
                fields.append(CustomDateField(field_name))
            elif isinstance(field, TimeField):
                fields.append(CustomTimeField(field_name))
            else:
                fields.append(field_name)

        self.helper.layout = CommonLayout(*tuple(fields))
