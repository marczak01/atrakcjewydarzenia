import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .models import Event, Attraction, Comment
from taggit.models import Tag
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import CommentForm, EventForm, AttractionForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify


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
    time_now = datetime.datetime.now

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.event = Event.published.get(id=pk)
            new_comment.save()
            # cd = comment_form.cleaned_data
            # comment = comment_form.save(commit=False)
            # Comment.objects.create(user=request.user, event=event, body=cd['body'])
            # comment.user_comment = request.user.id
            # comment.event_comment = event.id
            # comment.save()
    else:
        comment_form = CommentForm()
    comments = event.event_comments.all().order_by('-created_on')
    context = {
        'event': event,
        'src': src,
        'similar_posts':similar_posts,
        'time_now': time_now,
        'comment_form': comment_form,
        'comments':comments,
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


@login_required
def addEvent(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            cd = event_form.cleaned_data
            my_tags = cd['tags']           
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.status = 'PB'
            # event.slug = '-'.join([x for x in event.name])
            # event.slug = cd['name'].slice().join('-')
            event.slug = slugify(event.name)
            event.save()
            event.tags.add(*my_tags)
            return redirect('account:dashboard')
    else:
        event_form = EventForm()
    context = {
        'event_form': event_form,
    }
    return render(request, 'mainapp/events/event_form.html', context)


@login_required
def addAttraction(request):
    if request.method == 'POST':
        attraction_form = AttractionForm(request.POST)
        if attraction_form.is_valid():
            cd = attraction_form.cleaned_data
            my_tags = cd['tags']
            attraction = attraction_form.save(commit=False)
            attraction.created_by = request.user
            attraction.status = 'PB'
            attraction.slug = slugify(attraction.name)
            attraction.save()
            attraction.tags.add(*my_tags)

            return redirect('account:dashboard')
    else:
        attraction_form = AttractionForm()
    context = {
        'attraction_form': attraction_form,
    }
    return render(request, 'mainapp/attractions/attraction_form.html', context)