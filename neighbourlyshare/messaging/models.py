# messaging/models.py

from django.db import models
from userauth.models import Register  # Reference your custom user model

class Message(models.Model):
    sender = models.ForeignKey(Register, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Register, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"
