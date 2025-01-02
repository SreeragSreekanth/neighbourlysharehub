from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import *
from django.contrib.auth.hashers import make_password

# Create your views here.
def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Fetch user by email
            user_obj = Register.objects.get(email=email)
            # Authenticate using the username
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')  # Replace '/' with your desired home view
            else:
                messages.error(request, 'Invalid email or password')
        except Register.DoesNotExist:
            messages.error(request, 'No account found with this email')

    return render(request, 'index.html', {'page_name': 'login'})

def aboutUs(request):
    print("about")

    fruits = ["apple","orange","grapes"]
    
    return render(request,'about.html',{ 'name': "Sreerag", 'fruits':fruits})

def userReg(request):
    if request.method == 'POST':
        # Fetching form data from the POST request

        password = request.POST.get('password')


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