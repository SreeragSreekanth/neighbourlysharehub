from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, ItemImage  # Make sure to import ItemImage


# Create your views here.
@login_required
def Displayitems(request):
    # Fetch all items and pass them to the template
    items = Item.objects.all()  # This fetches all Item objects
    return render(request, 'itemlist.html', {'items': items})  # Pass 'items' context to template


@login_required
def additem(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        images = request.FILES.getlist('images')  # Get all uploaded images

        # Create an item instance
        item = Item.objects.create(
            title=title,
            description=description,
            user=request.user  # Set the current logged-in user
        )

        # Save multiple images to the Item
        for image in images:
            # Save each image in the ItemImage model
            item_image = ItemImage.objects.create(image=image)
            item.images.add(item_image)  # Associate the image with the item

        item.save()  # Save the item after all images are added

        messages.success(request, 'Item added successfully!')
        return redirect('itemlist')  # Redirect to item list page or wherever you want

    return render(request, 'additem.html')

@login_required
def deleteitem(request, id):
    # Retrieve the item using the item_id
    item = get_object_or_404(Item, pk=id)

    # Check if the current user is the owner of the item (optional for security)
    if item.user == request.user:
        # Delete the item
        item.delete()
        messages.success(request, "The product has been deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this item.")

    # Redirect to the item list page after deletion
    return redirect('itemlist')