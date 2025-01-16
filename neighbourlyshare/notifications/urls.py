from django.urls import path
from . import views

urlpatterns = [
    # Route to display all notifications
    path('notifications/', views.notification_list, name='notification_list'),
    
    # Route to view details of a specific notification
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    
    # Route to mark a specific notification as read
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
    
    # Route to mark all notifications as read
    path('notifications/mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),  # Mark all as read
    path('notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),

]
