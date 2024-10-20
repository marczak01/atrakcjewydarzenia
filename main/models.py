from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length=200, blank=True, null=True)
    event_photo = models.ImageField(null=False, upload_to='static/img/events')
    description = models.TextField(max_length=5000, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='events')
    categories = models.ManyToManyField('Category')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    

