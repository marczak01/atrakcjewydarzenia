from .models import Comment, Event, Attraction
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'start_date', 'end_date', 'public_private', 'tags']


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = ['name', 'city', 'country', 'longitude', 'latitude', 'description', 'tags']
