from website.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse



class GameForm(forms.Form):
    name = forms.CharField(label = 'Game Name', max_length=255, required=True,
    error_messages={'required': 'Your game needs a name!'})
    url = forms.URLField(label = 'Url', max_length=255, required=True,
    error_messages={'required': 'Your game needs a URL!'})
    image_url = forms.URLField(label = 'Image Url', max_length=1000, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=1000, label = 'Description', required=True,
    error_messages={'required': 'Your game needs a description!'})
    price = forms.FloatField(label = 'Price (€)', required = True,
    error_messages={'required': 'Your game needs a price!', 'min_value':'your game cannot cost less than 0!', 'max_value': 'your game cannot cost more than 10000!'}, min_value = 0.0, max_value = 10000.0)
    category = forms.ChoiceField(label = 'Category', required=True, widget=forms.Select(), choices=CATEGORY_CHOICES,
    error_messages={'required': 'Your game needs a category!',})

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    self.fields[f_name].widget.attrs['class'] = "form-control error"


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First name', max_length=30, required=True)
    last_name = forms.CharField(label='Last name', max_length=50, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    self.fields[f_name].widget.attrs['class'] = "form-control error"

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
