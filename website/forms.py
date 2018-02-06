from website.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse

class GameForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label = 'Game Name', max_length=255, required=True,
    error_messages={'required': 'Your game needs a name!'})
    url = forms.URLField(widget=forms.TextInput(attrs={'class':'form-control'}), label = 'Url', max_length=255, required=True,
    error_messages={'required': 'Your game needs a URL!'})
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label = 'Description', required=True,
    error_messages={'required': 'Your game needs a description for some reason!'})
    price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control'}), label = 'Price', required = True,
    error_messages={'required': 'Your game needs a price!', 'min_value':'your game cannot cost less than 0!', 'max_value': 'your game cannot cost more than 10000!'}, min_value = 0.0, max_value = 10000.0)

"""
# WORK IN PROGRESS
class Verification(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def generate_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def send_code(self):
        connection = mail.get_connection()
        link = reverse('verify_email')
        to_be_sent = mail.EmailMessage(
            'Your verification code',
            'Please visit this link: ' + link,
            'admin@gamestore.com',
            [''],
            connection=connection
        )

    def save(self):
        pass
"""

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


    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
