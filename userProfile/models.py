from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    phone_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    