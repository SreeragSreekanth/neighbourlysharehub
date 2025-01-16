from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category  # Assuming Notification is a model that stores notifications
from itemlisting.models import Item
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

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
    total_categories = Category.objects.count()
    total_pending_items = Item.objects.filter(status='pending').count()
    total_approved_items = Item.objects.filter(status='approved').count()

    context = {
        'total_categories': total_categories,
        'total_pending_items': total_pending_items,
        'total_approved_items': total_approved_items,
    }

    return render(request, 'valuator.html', context)


@login_required
def item_management(request):
    """Display approved items excluding 'Uncategorized'."""
    items = Item.objects.filter(status='approved').exclude(category__isnull=True)
    return render(request, 'item_management.html', {'items': items})

@login_required
def approval_needed(request):
    """Display items that need approval."""
    items = Item.objects.filter(status='pending')
    return render(request, 'approval_needed.html', {'items': items})

@login_required
def view_item(request, item_id):
    """View and edit an item if it is pending approval."""
    item = get_object_or_404(Item, id=item_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if not item.status == 'approved':
            category_id = request.POST.get('category')
            if category_id:
                item.category = Category.objects.get(id=category_id)
            else:
                item.category = None
            item.save()
        return redirect('approval_needed')  # Redirect to approval needed list

    return render(request, 'view_item.html', {'item': item, 'categories': categories})

@login_required
def approve_item(request, item_id):
    """Approve an item and notify the user."""
    item = get_object_or_404(Item, id=item_id)
    item.status = 'approved'  # Set status to approved
    item.save()

    # Create notification for the user who posted the item
    Notification.objects.create(
        user=item.user,  # Use `item.user` to get the owner (referring to Register model)
        message=f"Your item '{item.title}' has been approved.",
    )

    messages.success(request, 'Item approved successfully!')
    return redirect('item_management')

@login_required
def reject_item(request, item_id):
    """Reject an item and notify the user."""
    item = get_object_or_404(Item, id=item_id)
    item.status = 'rejected'  # Set status to rejected
    item.save()

    # Create notification for the user who posted the item
    Notification.objects.create(
        user=item.user,  # Use `item.user` to get the owner (referring to Register model)
        message=f"Your item '{item.title}' has been rejected.",
    )

    messages.success(request, 'Item rejected successfully!')
    return redirect('approval_needed')
