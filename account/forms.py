from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Employee, Jobseeker, User, EmailOTP


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length = 15,
        min_length = 3,
        label = 'Username',
        required = True,
        widget = TextInput({
            'class' : 'form-control'
        })
    )
    
    password = CharField(
        max_length = 15,
        min_length = 4,
        label = 'Password',
        required = True,
        widget = PasswordInput({
            'class' : 'form-control'
        })
    )
    class Meta:
        model = User
        fields = ('username','password')


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['images','username','password','first_name','last_name','email','dob','phone','gender','location','bio','interest','qualification','rel_status','smoke','drinking']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'interest': forms.Textarea(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'rel_status': forms.Select(attrs={'class': 'form-control'}),
            'smoke': forms.Select(attrs={'class': 'form-control'}),
            'drinking': forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['images','first_name','last_name','email','dob','phone','gender','location','bio','interest','qualification','rel_status','smoke','drinking']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interest': forms.Textarea(attrs={'class': 'form-control','rows':3}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'rel_status': forms.Select(attrs={'class': 'form-control'}),
            'smoke': forms.Select(attrs={'class': 'form-control'}),
            'drinking': forms.Select(attrs={'class': 'form-control'}),
        }

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailOTP
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }


class OTPForm(forms.Form):
    email = forms.EmailField(required=True)
    otp = forms.CharField(max_length=6, required=True)



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['position', 'department', 'location']
        widgets = {
            'position' : forms.TextInput(attrs={'class': 'form-control'}),
            'department' : forms.TextInput(attrs={'class': 'form-control'}),
            'location' : forms.TextInput(attrs={'class': 'form-control'}),


        }


class JobseekerForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        fields = ['title','expertise_level']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'expertise_level' : forms.Select(attrs={'class': 'form-control'}),
        }