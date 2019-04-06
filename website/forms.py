from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
UserType= [
    ('Customer','Customer'),
    ('Publisher','Publisher'),
]

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    accountType = forms.CharField(label='User Type', widget=forms.Select(choices=UserType))

    class Meta:
        model = User
        fields =['username','email', 'password1','password2']

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(RegistrationForm, self).save(commit=True)
        user_profile = UserProfile(user=user, accountType=self.cleaned_data['accountType'])
        user_profile.save()
        return user, user_profile

