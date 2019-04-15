from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django import forms
from products.models import EBook, Chapter
from django.conf import settings

class DateInput(forms.DateInput):
    input_type = 'date'

class MyForm(forms.ModelForm):
    class Meta:
        model = EBook
        fields = '__all__'
        exclude=('bookurl',)
        widgets = {
            'published_date': DateInput(),
        }


class MyChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        exclude=('ebook',)
