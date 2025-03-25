from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="userprofile")
    profile_image = models.ImageField(upload_to="profile_images", blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

