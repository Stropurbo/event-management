from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core .validators import RegexValidator
# Create your models here.

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="userprofile")
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

"""

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to="profile_images",
        default="default.png",
        blank=True
    )
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  
                message="Phone number must be entered in the format: '+88'. Up to 11 digits allowed."
            )
        ]
    )

    def __str__(self):
        return self.username