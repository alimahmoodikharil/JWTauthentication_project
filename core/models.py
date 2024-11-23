from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomerUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(unique= True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    
    objects = CustomerUserManager()

    