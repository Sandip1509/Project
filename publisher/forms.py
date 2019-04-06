from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django import forms
from .models import EBook, Chapter


class DateInput(forms.DateInput):
    input_type = 'date'

class MyForm(forms.ModelForm):
    class Meta:
        model = EBook
        fields = '__all__'
        widgets = {
            'published_date': DateInput(),
        }