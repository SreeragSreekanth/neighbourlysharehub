# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification



@login_required
def notification_list(request):
    """
    Displays a list of notifications for the logged-in user.
    """
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': user_notifications})


@login_required
def notification_detail(request, notification_id):
    """View notification details and mark as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return render(request, 'notification_detail.html', {'notification': notification})

@login_required
def mark_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_dashboard')

@login_required
def mark_all_as_read(request):
    """
    Marks all notifications for the logged-in user as read.
    """
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    user_notifications.update(is_read=True)  # Bulk update for efficiency
    return redirect('notification_list')  # Redirect back to the notifications list
