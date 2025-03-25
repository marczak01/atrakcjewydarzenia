from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Event.Status.PUBLISHED)


class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # choices for public/private type of event
    # if event is public then everyone can join
    # if private then only people with invintation link/code can join (after typing code into field)
    class PubPriv(models.TextChoices):
        PUBLIC = 'PB', 'Public'
        PRIVATE = 'PV', 'Private'


    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    city = models.CharField(max_length=70, null=False, blank=False)
    country = models.CharField(max_length=70)
    longitude = models.FloatField(default=111.111)
    latitude = models.FloatField(default=111.111)
    description = models.TextField(max_length=3000)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    public_private = models.CharField(max_length=2, choices=PubPriv.choices, default=PubPriv.PUBLIC)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_posts')
    tags = TaggableManager()

    objects = models.Manager() # default manager
    published = PublishedManager() # non standard manager

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


    def __str__(self):
       return self.name

    def get_absolute_url(self):
        return reverse("mainapp:event_details", kwargs={"pk": self.pk})
    

# class Attraction(Event):
#     openhours = models.CharField( max_length=20)

#     def __str__(self):
#         return self.openhours


class Attraction(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    city = models.CharField(max_length=70, null=False, blank=True)
    country = models.CharField(max_length=70, null=False, blank=True)
    longitude = models.FloatField(default=15.432)
    latitude = models.FloatField(default=54.234)
    description = models.TextField(max_length=3000)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attractions_posts')
    tags = TaggableManager()


    objects = models.Manager() # default manager
    published = PublishedManager() # non standard manager

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
       return self.name

    def get_absolute_url(self):
        return reverse('mainapp:attraction_details', kwargs={'pk': self.id})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')
    body = models.TextField(max_length=300, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body