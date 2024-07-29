from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Employee, Jobseeker, User, EmailOTP


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length = 15,
        min_length = 4,
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


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['images','first_name','last_name','email','dob','phone','gender','location','bio','interest','qualification','rel_status','smoke','drinking']


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


class JobseekerForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        fields = ['title','expertise_level']