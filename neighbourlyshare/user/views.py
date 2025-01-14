from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Rating
from .forms import RatingForm
from notifications.models import Notification
from exchange.models import ExchangeRequest

@login_required
def user_dashboard(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    recent_requests = ExchangeRequest.objects.filter(
        offered_by=user
    ).select_related('requested_item', 'offered_item').order_by('-created_at')

    context = {
        'user': user,
        'notifications': notifications,
        'recent_requests': recent_requests,
    }
    return render(request, 'user.html', context)


@login_required
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
def delete_review(request, id):
    review = get_object_or_404(Rating, id=id)
    
    # Ensure the current user is the reviewer of the review
    if review.reviewer != request.user:
        return redirect('viewitem', id=review.item.id)
    
    if request.method == 'POST':
        review.delete()
        return redirect('viewitem', id=review.item.id)
    
    return render(request, 'confirm_delete_review.html', {'review': review})