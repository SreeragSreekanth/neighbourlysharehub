import os
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, ItemImage  # Make sure to import ItemImage
from userauth.models import Register
from django.core.paginator import Paginator



# Create your views here.
@login_required
def Displayitems(request):
    # Fetch all items (you can filter by user if needed)
    items = Item.objects.all()  # Fetch all items, or you can filter by user: Item.objects.filter(user=request.user)
    
    # Paginate items
    paginator = Paginator(items, 6)  # Show 6 items per page
    page_number = request.GET.get('page')  # Get the page number from URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the current page object

    return render(request, 'itemlist.html', {'page_obj': page_obj})  # Pass paginated items to template


@login_required
def additem(request):
    if request.method == 'POST':
        # Extract item details from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')  # Get all uploaded files

        # Save the item
        item = Item.objects.create(
            title=title,
            description=description,
            user=request.user
        )

        # Save each image related to the item
        for image in images:
            ItemImage.objects.create(item=item, image=image)

        return redirect('itemlist')  # Redirect to the item list page

    return render(request, 'additem.html')
    
@login_required
def deleteitem(request, id):
    # Retrieve the item using the item_id
    item = get_object_or_404(Item, pk=id)

    # Check if the current user is the owner of the item (optional for security)
    if item.user == request.user:
        # Delete related images
        for item_image in item.images.all():
            if item_image.image:
                # Delete the image file from the storage
                if os.path.exists(item_image.image.path):
                    os.remove(item_image.image.path)
            item_image.delete()

        # Delete the item itself
        item.delete()

        # Success message
        messages.success(request, "The product and its images have been deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this item.")

    # Redirect to the item list page after deletion
    return redirect('itemlist')

@login_required
def viewitem(request, id):
    item = get_object_or_404(Item, id=id)
    images = item.images.all()  # Fetch all associated images
    return render(request, 'viewitem.html', {'item': item, 'images': images})

@login_required
def edititem(request, id):
    # Get the item to be edited
    item = get_object_or_404(Item, pk=id)

    # Check if the user is the owner of the item
    if item.user != request.user:
        messages.error(request, "You are not authorized to edit this item.")
        return redirect('itemlist')

    if request.method == 'POST':
        # Update the item's details
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.save()

        # Handle image uploads
        new_images = request.FILES.getlist('images')  # Get new images
        for image in new_images:
            ItemImage.objects.create(item=item, image=image)

        messages.success(request, "Item updated successfully!")
        return redirect('viewitem', id=item.id)

    # Pass the item and its images to the template
    images = item.images.all()
    return render(request, 'edititem.html', {'item': item, 'images': images})

@login_required
def deleteitemimage(request, id):
    # Fetch the image
    image = get_object_or_404(ItemImage, pk=id)

    # Check if the current user is the owner of the item
    if image.item.user == request.user:
        # Delete the image file from the storage
        if image.image and os.path.exists(image.image.path):
            os.remove(image.image.path)
        image.delete()
        messages.success(request, "Image deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this image.")

    return redirect('edititem', id=image.item.id)
