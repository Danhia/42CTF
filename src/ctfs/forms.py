from django import forms

class submit_flag(forms.Form):
    flag    =   forms.CharField(label="Flag", max_length=100)
