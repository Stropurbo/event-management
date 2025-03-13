from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(db_index=True)
    time = models.TimeField(auto_now=True)
    location = models.CharField(max_length=250)
    status = models.CharField(max_length=30, choices= [
        ('UPCOMING', 'upcoming'),
        ('COMPLETED', 'Completed')
    ], default='UPCOMING', db_index=True)

    category = models.ForeignKey(
        Category, 
        on_delete= models.CASCADE, 
        default=1,
        db_index=True
        )
    
    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)    
    event = models.ManyToManyField(Event, related_name='participants')

    def __str__(self):
        return self.name
    