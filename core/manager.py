from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password

class CustomerUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email Field Must Be Set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password, hasher= 'pbkdf2_sha256')
        user.save(using= self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fileds):
        extra_fileds.setdefault('is_staff', True)
        extra_fileds.setdefault('is_superuser', True)

        if extra_fileds.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fileds.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email=email, password=password, **extra_fileds)