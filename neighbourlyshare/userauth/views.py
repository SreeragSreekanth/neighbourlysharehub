from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.hashers import make_password
from .models import Register  # Adjust import based on your actual models
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import email_verification_token
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from .decorators import role_required




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
                    return redirect('admin')  # Redirect to the Django admin panel

                elif user_obj.role == 'valuator':
                    return redirect('valuator')  # Redirect to valuator dashboard
                else:
                    return redirect('user')  # Redirect to regular user page

            else:
                messages.error(request, 'Invalid username or password')

        except Register.DoesNotExist:
            messages.error(request, 'No account found with this username')

    return render(request, 'index.html', {'page_name': 'login',})

def logout_view(request):
    logout(request) 
    return redirect('/login/')

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
                user.is_active = False
                user.save()

                send_verification_email(request, user)  # Send verification email

                messages.success(request, 'Registration successful! Please verify your email to activate your account.')
                # return redirect('/login/')  
        else:
            messages.error(request, 'Please fill all the fields correctly.')

    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form,'page_name': 'signup'})

def homeFun(request):
    return render(request,'home.html',{'page_name':'home'})


def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Verify your email'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)

    # Render the HTML template
    html_content = render_to_string('verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })

    # Create an email with both plain text and HTML content
    email = EmailMultiAlternatives(
        subject=subject,
        body="Please verify your email by clicking the link.",  # Fallback plain-text content
        from_email='no-reply@yourdomain.com',
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('/login/')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('/signup/')

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)