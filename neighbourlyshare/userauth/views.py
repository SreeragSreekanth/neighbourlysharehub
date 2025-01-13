from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.hashers import make_password
from .models import Register  # Adjust import based on your actual models

def Login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = Register.objects.get(username=username)

            # Authenticate user
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)  # Log the user in

                # Check if the user is a superuser
                if user.is_superuser:
                    return redirect('/admindash/')  # Redirect to the Django admin panel

                elif user_obj.role == 'valuator':
                    return redirect('/valuator/')  # Redirect to valuator dashboard
                else:
                    return redirect('/user/')  # Redirect to regular user page

            else:
                messages.error(request, 'Invalid username or password')

        except Register.DoesNotExist:
            messages.error(request, 'No account found with this username')

    return render(request, 'index.html', {'page_name': 'login',})

def logout_view(request):
    logout(request) 
    return redirect('/login/')

def aboutUs(request):
    print("about")

    fruits = ["apple","orange","grapes"]
    
    return render(request,'about.html',{ 'name': "Sreerag", 'fruits':fruits, 'page_name':'about'})

def userReg(request):
    if request.method == 'POST':
        password = request.POST.get('password')

        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if Register.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
            elif Register.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email address.')
            else:
                user = form.save(commit=False)
                user.password = make_password(password)  
                user.role = 'user'

                user.save()

                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('/login/')  
        else:
            messages.error(request, 'Please fill all the fields correctly.')

    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'page_name': 'signup', 'form': form,})

def homeFun(request):
    return render(request,'home.html',{'page_name':'home'})

def AdminDashboard(request):
    return render(request, 'admin.html', {'page_name': 'admin'})


def ValuatorDashboard(request):
    return render(request, 'valuator.html', {'page_name': 'valuator'})

