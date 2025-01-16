# complaints/models.py
from django.db import models
from userauth.models import Register

class Complaint(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # The user who filed the complaint
    resolved_by = models.ForeignKey(Register, null=True, blank=True, on_delete=models.SET_NULL, related_name='resolved_complaints')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
