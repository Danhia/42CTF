from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User

class UserInfosUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields=('portfolio_site',)
    def __init__(self, *args, **kwargs):
        super(UserInfosUpdateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

class UserPasswordChange(forms.ModelForm):
    class Meta:
        model = User
        fields=('password',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('username', 'email',)
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site',)
