import os
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, ItemImage  # Make sure to import ItemImage
from userauth.models import Register
from django.core.paginator import Paginator
from .forms import ItemForm, ItemImageForm
from django.forms import modelformset_factory





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
    ImageFormSet = modelformset_factory(
        ItemImage, 
        form=ItemImageForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        formset = ImageFormSet(
            request.POST, 
            request.FILES,
            queryset=ItemImage.objects.none()
        )

        if item_form.is_valid() and formset.is_valid():
            # Save the item
            item = item_form.save(commit=False)
            # Get the Register instance associated with the current user
            try:
                register_user = Register.objects.get(username=request.user.username)
                item.user = register_user  # Assign the Register instance
                item.save()

                # Save the images
                for form in formset:
                    if form.cleaned_data.get('image'):
                        image = form.save(commit=False)
                        image.item = item
                        image.save()

                messages.success(request, 'Item added successfully!')
                return redirect('itemlist')
            except Register.DoesNotExist:
                messages.error(request, 'User profile not found.')
                return redirect('itemlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        item_form = ItemForm()
        formset = ImageFormSet(queryset=ItemImage.objects.none())

    return render(request, 'additem.html', {
        'item_form': item_form,
        'image_formset': formset
    })




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
    images = item.images.all()  # Always fetch the latest images associated with the item
    return render(request, 'viewitem.html', {'item': item, 'images': images})


@login_required
def edititem(request, id):
    item = get_object_or_404(Item, pk=id)
    ImageFormSet = modelformset_factory(
        ItemImage, 
        form=ItemImageForm,
        extra=1,
        can_delete=True,
    )

    if item.user.username != request.user.username:
        messages.error(request, "You are not authorized to edit this item.")
        return redirect('itemlist')

    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item)
        image_formset = ImageFormSet(
            request.POST, 
            request.FILES,
            queryset=ItemImage.objects.filter(item=item)
        )
        
        if item_form.is_valid() and image_formset.is_valid():
            try:
                # Save the item
                edited_item = item_form.save()

                # Handle the formset
                instances = image_formset.save(commit=False)
                
                # Save new images
                for instance in instances:
                    if instance.image:  # Only save if there's actually an image
                        instance.item = edited_item
                        instance.save()
                
                # Handle deletions
                for obj in image_formset.deleted_objects:
                    if obj.image:
                        if obj.image.path and os.path.exists(obj.image.path):
                            try:
                                os.remove(obj.image.path)
                            except Exception as e:
                                print(f"Error deleting image file: {e}")
                    obj.delete()

                # Save the formset to process any deletions
                image_formset.save()

                messages.success(request, "Item updated successfully!")
                return redirect('viewitem', id=item.id)
                
            except Exception as e:
                messages.error(request, f"Error saving changes: {str(e)}")
        else:
            for form in image_formset:
                if form.errors:
                    print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        item_form = ItemForm(instance=item)
        image_formset = ImageFormSet(queryset=ItemImage.objects.filter(item=item))

    return render(request, 'edititem.html', {
        'item_form': item_form,
        'image_formset': image_formset,
        'item': item,
        'existing_images': ItemImage.objects.filter(item=item)
    })

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
