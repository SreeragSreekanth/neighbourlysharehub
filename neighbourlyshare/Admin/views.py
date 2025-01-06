from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ValuatorForm
from userauth.models import Register
from django.contrib import messages

def add_valuator(request):
    print(request.method == 'POST')
    if request.method == 'POST':
        form = ValuatorForm(request.POST)
        if form.is_valid():
            # Set the role to 'valuator' before saving
            valuator = form.save(commit=False)
            valuator.role = 'valuator'
            valuator.set_password(form.cleaned_data['password'])  # Make sure to hash the password
            valuator.save()

            messages.success(request, 'Valuator added successfully!')
            return redirect('valuatorlist')  # Redirect to the valuator list page (adjust URL name as needed)
    else:
        form = ValuatorForm()
    return render(request, 'addvaluator.html', {'form': form})


@login_required
def AdminDashboard(request):
    return render(request, 'admin.html',{})

def Valuatorlist(request):
    # Query to get all valuators (users with 'valuator' role)
    valuators = Register.objects.filter(role='valuator')
    
    return render(request, 'valuatorlist.html', {'valuators': valuators})

def Userlist(request):
    # Query to get all valuators (users with 'valuator' role)
    users = Register.objects.filter(role='user')
    
    return render(request, 'userlist.html', {'users': users})

def adduser(request):
    print(request.method == 'POST')
    if request.method == 'POST':
        form = ValuatorForm(request.POST)
        if form.is_valid():
            # Set the role to 'valuator' before saving
            user = form.save(commit=False)
            user.role = 'user'
            user.set_password(form.cleaned_data['password'])  # Make sure to hash the password
            user.save()

            messages.success(request, 'User added successfully!')
            return redirect('userlist')  # Redirect to the valuator list page (adjust URL name as needed)
    else: 
        form = ValuatorForm()
    return render(request,'adduser.html',{'form':form })

def deleteuser(request, id):
    # Try to get the user by ID
    try:
        user = Register.objects.get(id=id)
    except Register.DoesNotExist:
        # If the user doesn't exist, redirect to the user list page
        return redirect('userlist')
    
    # If user exists, delete the user
    user.delete()
    
    # Redirect back to the user list page after deletion
    return redirect('userlist')

def deletevaluator(request, id):
    # Try to get the user by ID
    try:
        valuator = Register.objects.get(id=id)
    except Register.DoesNotExist:
        # If the user doesn't exist, redirect to the user list page
        return redirect('valuatorlist')
    
    # If user exists, delete the user
    valuator.delete()
    
    # Redirect back to the user list page after deletion
    return redirect('valuatorlist')