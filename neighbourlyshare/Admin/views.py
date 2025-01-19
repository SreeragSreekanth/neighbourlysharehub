from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ValuatorForm, EditForm
from userauth.models import Register
from django.contrib import messages
from itemlisting.models import Item,ItemImage
from django.contrib.auth.hashers import make_password
from complaints.models import Complaint
from category_management.models import Category
from user.models import Rating
from exchange.models import ExchangeRequest
from userauth.decorators import superuser_required


@login_required
@superuser_required
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
@superuser_required
def AdminDashboard(request):
    total_users = Register.objects.filter(role='user').count()
    total_items = Item.objects.filter(status='approved').count()
    total_valuators = Register.objects.filter(role='valuator').count()
    total_transactions = ExchangeRequest.objects.filter(status='accepted').count()  # Adjust based on your status field


    context = {
        'total_users': total_users,
        'total_items': total_items,
        'total_valuators': total_valuators,
        'total_transactions': total_transactions,
    }

    return render(request, 'admin.html', context)


@login_required
@superuser_required
def Valuatorlist(request):
    # Query to get all valuators (users with 'valuator' role)
    valuators = Register.objects.filter(role='valuator')
    
    return render(request, 'valuatorlist.html', {'valuators': valuators})


@login_required
@superuser_required
def Userlist(request):
    # Query to get all valuators (users with 'valuator' role)
    users = Register.objects.filter(role='user')
    
    return render(request, 'userlist.html', {'users': users})


@login_required
@superuser_required
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
@superuser_required
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
@superuser_required
def edituser(request, id):
    # Get the user object or return a 404 if not found
    user = get_object_or_404(Register, id=id)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=user)  # Bind form with data and user instance
        if form.is_valid():
            form.save()  # Save the changes
            messages.success(request, 'Changes saved successfully!')
            return redirect('userlist')  # Redirect to the user list page
        else:
            messages.error(request, 'Error saving changes. Please check the form.')
    else:
        form = EditForm(instance=user)  # Prepopulate the form with user data

    return render(request, 'edituser.html', {'form': form, 'user': user})



@login_required
@superuser_required
def editvaluator(request, id):
    valuator = get_object_or_404(Register, id = id)  # Get user by ID
    if request.method == 'POST':
        password = request.POST.get('password')
        form = EditForm(request.POST, instance=valuator)
        password = request.POST.get('password')
  # Pass the existing user to the form
        if form.is_valid():
            password = make_password(password)
            form.save()  # Save the updated data
            messages.success(request, 'Save changes successfully!')
            return redirect('valuatorlist')  # Redirect to the user management page
    else:
        form = EditForm(instance=valuator)  # Prepopulate form with existing user data
    return render(request, 'editvaluator.html', {'form': form, 'valuator': valuator,})


@login_required
@superuser_required
def Userlist(request):
    # Query to get all valuators (users with 'valuator' role)
    users = Register.objects.filter(role='user')
    return render(request, 'userlist.html', {'users': users})



@login_required
@superuser_required
def adminitem(request):
    """View to display approved items with valid categories (excluding 'Uncategorized')."""
    items = Item.objects.all
    return render(request, 'adminitem.html', {'items': items})



@login_required
@superuser_required
def complaintlist(request):
    """Shows a list of pending complaints."""
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaintview.html', {'complaints': complaints})



@login_required
@superuser_required
def admin_viewitem(request, id):
    item = get_object_or_404(Item, id=id)
    ratings = Rating.objects.filter(item=item).order_by('-created_at')
    reviews = ratings  # Assign reviews to ratings

    images = ItemImage.objects.filter(item=item)
    
    return render(request, 'admin_viewitem.html', {
        'item': item,
        'ratings': ratings,
        'reviews': reviews,
        'images': images,
        'range_5': range(1, 6),  # Pass a range to the template
    })


@login_required
@superuser_required
def transactionlist(request):
    """Shows a list of accepted transactions."""
    transactions = ExchangeRequest.objects.filter(status='accepted').order_by('-accepted_at')  # Ordering by accepted date
    return render(request, 'transactions.html', {'transactions': transactions})
   
