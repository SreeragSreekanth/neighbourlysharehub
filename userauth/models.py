from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Register(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('valuator', 'Valuator'),
    ]
    role = models.CharField(max_length=255,null=True,choices=ROLE_CHOICES,default='user')
    phone_number = models.CharField(max_length=10, null=True)

    