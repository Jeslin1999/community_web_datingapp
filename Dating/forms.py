from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User, Genderselect, Message, Media


class GenderselectForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    ]
    genderselect = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Genderselect
        fields = ['genderselect']


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['media_type', 'file',]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 1000}),
        }