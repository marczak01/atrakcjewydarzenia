from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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


    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    city = models.CharField(max_length=70, null=False, blank=False)
    country = models.CharField(max_length=70)
    longitude = models.FloatField(default=15.432)
    latitude = models.FloatField(default=54.234)
    description = models.TextField(max_length=3000)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    public_private = models.CharField(max_length=2, choices=PubPriv.choices, default=PubPriv.PUBLIC)
    event_photo = models.ImageField(upload_to='events/%Y/%m/%d/',
                              blank=True)
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

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    city = models.CharField(max_length=70, null=False, blank=True)
    country = models.CharField(max_length=70, null=False, blank=True)
    longitude = models.FloatField(default=15.432)
    latitude = models.FloatField(default=54.234)
    description = models.TextField(max_length=3000)
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    attraction_photo = models.ImageField(upload_to='attractions/%Y/%m/%d/',
                              blank=True)
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
    body = models.TextField(max_length=300, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')

    def __str__(self):
        return self.body


class Followed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followed')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_followed')
    follow_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.username} follow {self.event.name}"

def rating_scope(value):
    if value >= 1 and value <= 5: pass
    else: raise ValidationError(f"{value} is not between 1 and 5. Correct it please.")

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_ratings')
    rate = models.IntegerField(validators=[rating_scope])
    body = models.TextField(max_length=250, blank=True, null=True)
    rating_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} ocenia to wydarzenie na {self.rate}"
