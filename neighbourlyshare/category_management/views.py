from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category
from itemlisting.models import Item  # Assuming 'itemlisting' is the app for items
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
    return render(request, 'category_add.html', {'form': form})

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
    return render(request, 'category_edit.html', {'form': form, 'category': category})

@login_required
def category_delete(request, pk):
    """View to delete a category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'category_delete.html', {'category': category})


@login_required
def assign_category(request, item_id):
    """View to assign a category to an item."""
    item = get_object_or_404(Item, pk=item_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_id)
        item.category = category
        item.save()
        messages.success(request, 'Category assigned successfully!')
        return redirect('item_detail', pk=item.id)  # Redirect to item detail view
    return render(request, 'assign_category.html', {'item': item, 'categories': categories})

@login_required
def ValuatorDashboard(request):
    return render(request, 'valuator.html', {})