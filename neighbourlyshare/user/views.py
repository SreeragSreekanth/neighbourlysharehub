from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Rating
from .forms import RatingForm


@login_required
def Userdashboard(request):
    return render(request, 'user.html',{})

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