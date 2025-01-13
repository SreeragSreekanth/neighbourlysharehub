from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category
from itemlisting.models import Item ,ItemImage # Assuming 'itemlisting' is the app for items
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required

@login_required
def category_list(request):
    """View to list all categories."""
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_add(request):
    """View to add a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_add.html', {'form': form, })

@login_required
def category_edit(request, pk):
    """View to edit an existing category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_edit.html', {'form': form, 'category': category,})

@login_required
def category_delete(request, pk):
    """View to delete a category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'category_delete.html', {'category': category,})




@login_required
def ValuatorDashboard(request):
    # Count of categories
    category_count = Category.objects.count()  # Count all categories
    pending_items_count = Item.objects.filter(approved='pending').count()  # Count pending items
    approved_items_count = Item.objects.filter(approved='approved').count()  # Count approved items

    # Pass the counts to the template
    context = {
        'category_count': category_count,
        'pending_items_count': pending_items_count,
        'approved_items_count': approved_items_count,
    }
    
    return render(request, 'valuator.html', context)

@login_required
def item_management(request):
    """View to display approved items with valid categories (excluding 'Uncategorized')."""
    items = Item.objects.filter(status='approved').exclude(category__isnull=True)
    return render(request, 'item_management.html', {'items': items})

@login_required
def approval_needed(request):
    """View to display items that are not yet approved."""
    items = Item.objects.filter(status='pending')  # Show items that are pending approval
    return render(request, 'approval_needed.html', {'items': items})

@login_required
def view_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        # If the item is not approved yet, we allow the category change to be made
        if not item.approved:
            category_id = request.POST.get('category')
            if category_id:
                # If a category is selected, we update the category
                item.category = Category.objects.get(id=category_id)
            else:
                # Reset to Uncategorized if no category is selected
                item.category = None
            item.save()

        return redirect('approval_needed')  # Redirect to the approval needed list

    return render(request, 'view_item.html', {'item': item, 'categories': categories})

@login_required
def approve_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = 'approved'  # Set status to approved
    item.save()
    return redirect('item_management')  # Redirect to the item management page

@login_required
def reject_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.status = 'rejected'  # Set status to rejected
    item.save()
    return redirect('approval_needed')  # Redirect to the approval needed page
