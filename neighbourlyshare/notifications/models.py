from django.db import models
from userauth.models import Register

# models.py
# notifications/models.py
class Notification(models.Model):
    APPROVAL = 'approval'
    REJECTION = 'rejection'
    NEW_MESSAGE = 'new_message'
    PENDING = 'pending'
    RESOLVED_COMPLAINT = 'resolved_complaint'  # Added type for resolved complaints
    NEW_ITEM = 'new_item'

    NOTIFICATION_TYPES = [
        (APPROVAL, 'Item Request Approved'),
        (REJECTION, 'Item Request Rejected'),
        (NEW_MESSAGE, 'New Message Received'),
        (PENDING, 'Item Request Pending'),
        (RESOLVED_COMPLAINT, 'Complaint Resolved'),  # Added resolved complaint
        (NEW_ITEM, 'New Item Available'),
    ]
    
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default=PENDING
    )

    def __str__(self):
        return f"{self.notification_type} - {self.user.username}"
