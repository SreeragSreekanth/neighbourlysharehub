from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.hashers import make_password

# Create your views here.
def Login(request):
    return render(request,'index.html',{'page_name': 'login'})

def aboutUs(request):
    print("about")

    fruits = ["apple","orange","grapes"]
    
    return render(request,'about.html',{ 'name': "Sreerag", 'fruits':fruits})

def userReg(request):
    if request.method == 'POST':
        # Fetching form data from the POST request
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(password)
            user.save()

        else:
            print(form.errors)
    else:

        form = RegisterForm()
        # Password validation: check if passwords match

        # Render the signup page for GET requests
    return render(request, 'signup.html', {'page_name': 'signup','form':form})

def homeFun(request):
    return render(request,'home.html')