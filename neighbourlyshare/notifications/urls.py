from django.urls import path
from . import views

urlpatterns = [
    # Route to display all notifications
    path('notifications/', views.notification_list, name='notification_list'),
    
    # Route to view details of a specific notification
    path('notifications/<int:notification_id>/', views.notification_detail, name='notification_detail'),
    
    # Route to mark a notification as read
    path('notifications/<int:notification_id>/mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),  # Mark all as read

]

