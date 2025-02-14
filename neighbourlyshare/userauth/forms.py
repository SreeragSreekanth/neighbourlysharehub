from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Register
from django.core.validators import MinLengthValidator


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text=""
    )
    first_name = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
        help_text=""
    )
    last_name = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        help_text=""
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        help_text=""
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
        help_text="",
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        help_text="",
        label="Confirm your password"
    )
    phone_number = forms.CharField(
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        help_text="Phone number must be 10 digits.",
        validators=[MinLengthValidator(10)],
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','phone_number']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
        help_text=""
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        help_text=""
    )
