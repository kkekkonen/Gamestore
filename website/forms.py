from website.models import *
from django.forms import ModelForm
from django import forms

class GameForm(forms.Form):
    name = forms.CharField(label = 'Game Name', max_length=255, required = True,
    error_messages={'required': 'Your game needs a name!'})
    url = forms.URLField(label = 'Url', max_length=255, required = True,
    error_messages={'required': 'Your game needs a URL!'})
    description = forms.CharField(label = 'Url', required = True,
    error_messages={'required': 'Your game needs a description for some reason!'})
