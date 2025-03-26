from .models import Comment, Event, Attraction
from django import forms
from taggit.forms import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {'start_date': forms.SelectDateWidget(), 'end_date': forms.SelectDateWidget()}
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'start_date', 'end_date', 'public_private', 'tags']


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        # widgets = {'tags': TagWidget()}
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'tags']
        
        
