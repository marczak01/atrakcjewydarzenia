from django.db import models
from django.urls import reverse


# Create your models here.
class EventModel(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title

