from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    timezone = models.CharField(max_length=20, default='UTC')

    def __str__(self):
        return self.username

class Recurence(models.TextChoices):
    NONE = 'none', 'None'
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'

class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=50)
    attendees = models.ManyToManyField(User, related_name='events')
    recurrence = models.CharField(max_length=10, choices=Recurence.choices, default=Recurence.NONE)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f'{self.title}'
    
    def is_conflicting(self, user):
        overlapping = Event.objects.filter(attendees=user, start_time__lt=self.end_time, end_time__gt=self.start_time).exclude(id=self.id)
        return overlapping.exists()