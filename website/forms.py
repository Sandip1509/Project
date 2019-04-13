from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

userType = [
    ('Customer','Customer'),
    ('Publisher','Publisher'),
]


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields=['username','email','password1','password2']

class RegistrationForm(forms.ModelForm):
    accountType = forms.CharField(label='Account Type', widget=forms.Select(choices=userType))

    class Meta:
        model = UserProfile
        fields=['accountType']

class LogInForm(AuthenticationForm):
    username = forms.CharField(max_length=500)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
