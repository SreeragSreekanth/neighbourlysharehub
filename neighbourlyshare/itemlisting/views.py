import os
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item, ItemImage  # Make sure to import ItemImage
from userauth.models import Register
from django.core.paginator import Paginator
from .forms import ItemForm, ItemImageForm, ItemSearchForm
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.db.models import Q
from user.forms import RatingForm
from user.models import Rating
from notifications.utils import create_notification
from userauth.decorators import role_required






# Create your views here.
@login_required
@role_required(['user'])
def Displayitems(request):
    # Fetch all items (you can filter by user if needed)
    items = Item.objects.filter(user=request.user)
    
    # Paginate items
    paginator = Paginator(items, 6)  # Show 6 items per page
    page_number = request.GET.get('page')  # Get the page number from URL query parameters
    page_obj = paginator.get_page(page_number)  # Get the current page object

    return render(request, 'itemlist.html', {'page_obj': page_obj, })  # Pass paginated items to template


@login_required
@role_required(['user'])
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
        'image_formset': formset,
    })




@login_required
@role_required(['user'])
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
@role_required(['user'])
def viewitem(request, id):
    item = get_object_or_404(Item, id=id)
    ratings = Rating.objects.filter(item=item).order_by('-created_at')
    reviews = ratings  # Assign reviews to ratings

    images = ItemImage.objects.filter(item=item)
    existing_rating = Rating.objects.filter(item=item, reviewer=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        form = RatingForm(request.POST, instance=existing_rating) if existing_rating else RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.item = item
            rating.reviewer = request.user
            rating.reviewee = item.user
            rating.save()
    else:
        form = RatingForm(instance=existing_rating if existing_rating else None)

    return render(request, 'viewitem.html', {
        'item': item,
        'ratings': ratings,
        'reviews': reviews,
        'form': form,
        'images': images,
        'range_5': range(1, 6),  # Pass a range to the template
    })



@login_required
@role_required(['user'])
def edititem(request, id):
    item = get_object_or_404(Item, pk=id)
    
    # Create the modelformset for the ItemImage
    ImageFormSet = modelformset_factory(
        ItemImage, 
        form=ItemImageForm,
        extra=1,  # Allow adding 1 new form at a time
        can_delete=True,
    )

    # Ensure the user is authorized to edit this item
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
                edited_item.status = 'pending'  # Set item status to 'pending'
                edited_item.save()

                # Handle image additions and updates
                instances = image_formset.save(commit=False)
                for instance in instances:
                    if instance.image:  # Only save if there's an image
                        instance.item = edited_item
                        instance.save()

                # Handle deletions (remove images that are marked for deletion)
                for obj in image_formset.deleted_objects:
                    if obj.image:
                        if obj.image.path and os.path.exists(obj.image.path):
                            try:
                                os.remove(obj.image.path)  # Delete the image file from filesystem
                            except Exception as e:
                                print(f"Error deleting image file: {e}")
                    obj.delete()

                # Save the formset (this handles new and deleted images)
                image_formset.save()

                messages.success(request, "Item updated successfully!")
                return redirect('itemlist')

            except Exception as e:
                messages.error(request, f"Error saving changes: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
            for form in image_formset:
                if form.errors:
                    print("Form errors:", form.errors)
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
@role_required(['user'])
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

@login_required
@role_required(['user'])
def item_listing(request):
    # Instantiate the form and process user input
    form = ItemSearchForm(request.GET)
    
    # Filter only approved items
    items = Item.objects.filter(status='approved')

    if form.is_valid():
        query = form.cleaned_data['q']
        category_filter = form.cleaned_data['category']
        sort_by = form.cleaned_data['sort_by']

        # Search filtering
        if query:
            # Filter by title and description separately
            items = items.filter(title__icontains=query) | items.filter(description__icontains=query)

        # Category filter
        if category_filter:
            items = items.filter(category=category_filter)

        # Sorting
        if sort_by == 'date_asc':
            items = items.order_by('date_posted')
        elif sort_by == 'date_desc':
            items = items.order_by('-date_posted')
        elif sort_by == 'title':
            items = items.order_by('title')

    # Provide the form and the filtered items to the template
    return render(request, 'item_listing.html', {'form': form, 'items': items})
