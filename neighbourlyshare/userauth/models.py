from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Register(AbstractUser):
    role = models.CharField(max_length=255,null=True)
    phone_number = models.CharField(max_length=10, null=True)


    