from .models import Comment, Event, Attraction, Rating, News
from django import forms
from taggit.forms import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
        # widgets = {'start_date': forms.DateTimeInput(), 'end_date': forms.DateTimeInput()}
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'start_date', 'end_date', 'public_private', 'tags', 'event_photo']


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        # widgets = {'tags': TagWidget()}
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'tags', 'attraction_photo']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate', 'body']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body']