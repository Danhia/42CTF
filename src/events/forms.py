from django import forms
from .models import Team

class submit_flag(forms.Form):
    flag    =   forms.CharField(label="Flag", max_length=100)

class create_team(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = Team
        fields = ('name','password')

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields=('name', 'password',)
    def __init__(self, *args, **kwargs):
        super(TeamUpdateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True