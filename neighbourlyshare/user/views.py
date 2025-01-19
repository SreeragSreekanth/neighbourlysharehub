from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Rating
from .forms import RatingForm
from exchange.models import ExchangeRequest
from itemlisting.models import Item
from exchange.models import ExchangeRequest
from notifications.models import Notification
from userauth.decorators import role_required

@login_required
@role_required(['user'])
def user_dashboard(request):
    approved_items = Item.objects.filter(user=request.user, status='approved')  # Fetch approved items for the logged-in user.

    context = {
        'items_posted_count': Item.objects.filter(user=request.user).count(),
        'accepted_requests_count': ExchangeRequest.objects.filter(offered_by=request.user, status='accepted').count(),
        'requests_received_count': ExchangeRequest.objects.filter(requested_item__user=request.user).count(),
        'notifications': Notification.objects.filter(user=request.user).order_by('-created_at'),
        'recent_requests': ExchangeRequest.objects.filter(requested_item__user=request.user).order_by('-created_at')[:5],
        'approved_items': approved_items,  # Add approved items to the context.
    }

    return render(request, 'user.html', context)






@login_required
@role_required(['user'])
def edit_review(request, id):
    review = get_object_or_404(Rating, id=id)
    
    # Ensure the current user is the reviewer of the review
    if review.reviewer != request.user:
        return redirect('viewitem', id=review.item.id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('viewitem', id=review.item.id)
    else:
        form = RatingForm(instance=review)
    
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
@role_required(['user'])
def delete_review(request, id):
    review = get_object_or_404(Rating, id=id)
    
    # Ensure the current user is the reviewer of the review
    if review.reviewer != request.user:
        return redirect('viewitem', id=review.item.id)
    
    if request.method == 'POST':
        review.delete()
        return redirect('viewitem', id=review.item.id)
    
    return render(request, 'confirm_delete_review.html', {'review': review})


def privacy(request):
    return render(request,'privacy.html')

def faq(request):
    return render(request,'faq.html')
