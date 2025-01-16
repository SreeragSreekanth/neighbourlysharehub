# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse



@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': notifications})

@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    # Mark as read if necessary
    notification.is_read = True
    notification.save()
    
    return render(request, 'notification_detail.html', {'notification': notification})

# views.py
@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')


@login_required
def mark_all_as_read(request):
    """
    Marks all notifications for the logged-in user as read.
    """
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    user_notifications.update(is_read=True)  # Bulk update for efficiency
    return redirect('notification_list')  # Redirect back to the notifications list

@login_required
def unread_notifications_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'unread_count': count})
    return JsonResponse({'unread_count': 0})