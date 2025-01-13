from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ValuatorForm
from userauth.models import Register
from django.contrib import messages
from itemlisting.models import Item,ItemImage
from django.contrib.auth.hashers import make_password


@login_required
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
    return render(request, 'addvaluator.html', {'form': form,})


@login_required
def AdminDashboard(request):
    return render(request, 'admin.html',{})

@login_required

def Valuatorlist(request):
    # Query to get all valuators (users with 'valuator' role)
    valuators = Register.objects.filter(role='valuator')
    
    return render(request, 'valuatorlist.html', {'valuators': valuators})


@login_required
def Userlist(request):
    # Query to get all valuators (users with 'valuator' role)
    users = Register.objects.filter(role='user')
    
    return render(request, 'userlist.html', {'users': users})

@login_required
def adduser(request):
    print(request.method == 'POST')
    if request.method == 'POST':
        form = ValuatorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.set_password(form.cleaned_data['password'])  # Make sure to hash the password
            user.save()

            messages.success(request, 'User added successfully!')
            return redirect('userlist')  # Redirect to the valuator list page (adjust URL name as needed)
    else: 
        form = ValuatorForm()
    return render(request,'adduser.html',{'form':form, })

@login_required
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

@login_required
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

@login_required
def edituser(request, id):
    user = get_object_or_404(Register, id = id)  # Get user by ID
    if request.method == 'POST':
        form = ValuatorForm(request.POST, instance=user)  # Pass the existing user to the form
        if form.is_valid():
            password = make_password(password)
            form.save()  # Save the updated data
            messages.success(request, 'User added successfully!')
            return redirect('userlist')  # Redirect to the user management page
    else:
        form = ValuatorForm(instance=user)  # Prepopulate form with existing user data
    return render(request, 'edituser.html', {'form': form, 'user': user, })

@login_required
def editvaluator(request, id):
    valuator = get_object_or_404(Register, id = id)  # Get user by ID
    if request.method == 'POST':
        password = request.POST.get('password')
        form = ValuatorForm(request.POST, instance=valuator)
        password = request.POST.get('password')
  # Pass the existing user to the form
        if form.is_valid():
            password = make_password(password)
            form.save()  # Save the updated data
            messages.success(request, 'Valuator added successfully!')
            return redirect('valuatorlist')  # Redirect to the user management page
    else:
        form = ValuatorForm(instance=valuator)  # Prepopulate form with existing user data
    return render(request, 'editvaluator.html', {'form': form, 'valuator': valuator,})

@login_required
def Userlist(request):
    # Query to get all valuators (users with 'valuator' role)
    users = Register.objects.filter(role='user')
    return render(request, 'userlist.html', {'users': users})

@login_required
def adminitem(request):
    """View to display approved items with valid categories (excluding 'Uncategorized')."""
    items = Item.objects.all
    return render(request, 'adminitem.html', {'items': items})