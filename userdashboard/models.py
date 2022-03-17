from datetime import datetime
from django.db import models

# Create your models here.

class userDashboard(models.Model):
    username=models.CharField(max_length=20, blank=True, default='')
    name=models.CharField(max_length=30, blank=True, default='')
    email=models.EmailField(max_length=50, blank=True, default='')
    number=models.CharField(max_length=15, blank=True, default='')
    collegeName=models.CharField(max_length=100, blank=True, default='')
    city=models.CharField(max_length=100, blank=True, default='')
    ambassador=models.CharField(max_length=50, blank=True, default='')
    events_registered=models.CharField(max_length=100, blank=True, default='')
    datestamp = models.DateField(auto_now=True, blank=True)
    timestamp = models.TimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.username