import datetime
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from .models import Event, Attraction
from taggit.models import Tag
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    templateFileName = 'mainapp/index.html'
    context = {

    }
    return render(request, templateFileName, context)

def welcome(request):
    templateFileName = 'mainapp/welcome.html'
    context = {

    }
    return render(request, templateFileName, context)

def events(request, tag_slug=None):
    templateFileName = 'mainapp/events/events.html'
    events_list = Event.published.all()
    paginator = Paginator(events_list, 3)
    page_number = request.GET.get('page', 1)
    events = paginator.page(page_number)
    tag = None
    time_now = timezone.now
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        events = events_list.filter(tags__in=[tag])

    context = {
        'events': events,
        'tag': tag,
        'time_now': time_now,

    }
    return render(request, templateFileName, context)

def event_details(request, pk):
    templateFileName = 'mainapp/events/eventDetails.html'
    event = Event.published.get(id=pk)
    src = f"https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d2128.1919194050733!2d{str(event.longitude)}!3d{str(event.latitude)}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zNTTCsDEwJzUyLjciTiAxNcKwMzQnMjcuOSJF!5e1!3m2!1spl!2spl!4v1741851245110!5m2!1spl!2spl"
    event_tags_ids = event.tags.values_list('id', flat=True)
    similar_posts = Event.published.filter(tags__in=event_tags_ids).exclude(id=event.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    time_now = timezone.now
    context = {
        'event': event,
        'src': src,
        'similar_posts':similar_posts,
        'time_now': time_now,

    }
    return render(request, templateFileName, context)

def attractions(request):
    templateFileName = 'mainapp/attractions/attractions.html'
    attractions = Attraction.published.all()
    context = {
        'attractions': attractions,
    }
    return render(request, templateFileName, context)

def attraction_details(request, pk):
    templateFileName = 'mainapp/attractions/attractionDetails.html'
    context = {

    }
    return render(request, templateFileName, context)