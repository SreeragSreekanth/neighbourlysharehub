from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
            model = Register
            fields = ['role','username','first_name','last_name','email','phone_number','password']
            help_texts={
                  'username':''
            }
            widgets = {
            'role': forms.Select(attrs={'class': 'form-select', 'aria-label': 'Role'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
            

    