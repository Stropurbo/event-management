from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core .validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to="profile_images",
        default='profile_images/default.png',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  
                message="Phone number must be entered in the format: '+88'. Up to 11 digits allowed."
            )
        ], blank=True, null=True
    )
    objects = CustomUserManager() 



    def __str__(self):
        return self.username