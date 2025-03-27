from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(db_index=True)
    time = models.TimeField()
    location = models.CharField(max_length=250)
    email = models.EmailField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=30, choices= [
        ('UPCOMING', 'upcoming'),
        ('COMPLETED', 'Completed')
    ], default='UPCOMING', db_index=True)

    asset = models.ImageField(upload_to='event_asset', blank=True, null=True)
    
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="rsvp_event", 
        blank=True
        )

    category = models.ForeignKey(
        Category, 
        on_delete= models.CASCADE, 
        default=1,
        db_index=True
        )
   

    def __str__(self):
        return self.name