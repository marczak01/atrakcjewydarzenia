from datetime import datetime, timedelta
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from .models import Event, Attraction, Comment, Followed, Rating, News
from taggit.models import Tag
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import CommentForm, EventForm, AttractionForm, RatingForm, NewsForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

# Create your views here.

def home(request, selected='topevents'):
    templateFileName = 'mainapp/index.html'
    events = Event.objects.all()[:3]
    top_events = Event.objects.all()[:4]
    top_destinations = Event.objects.values('city').annotate(destination_count=Count('city')).order_by('-destination_count', 'city')[:8]
    nearby_events = Event.objects.all()[4:8]
    if selected == 'topevents':
        active = selected
        selected = top_events
    elif selected == 'nearby':
        active = selected
        selected = nearby_events
    time_now = timezone.now
    context = {
        'events': events,
        'selected':selected,
        'active':active,
        'time_now': time_now,
        'top_destinations': top_destinations,
    }
    return render(request, templateFileName, context)

def welcome(request):
    templateFileName = 'mainapp/welcome.html'
    context = {

    }
    return render(request, templateFileName, context)

def events(request, weekday=None, tag_slug=None, city=None, monthday=None, day=None, this_week=None, by_month=None):
    page = 'events'

    weekdays = {'monday' : 2,
                'tuesday': 3,
                'wednesday': 4,
                'thursday': 5,
                'friday': 6,
                'saturday': 7,
                'sunday': 1}

    templateFileName = 'mainapp/events/events.html'
    events = Event.published.all()
    no_events = events.count()
    # paginator = Paginator(events_list, 3)
    # page_number = request.GET.get('page', 1)
    # events = paginator.page(page_number)
    tag = None
    time_now = timezone.now
    date_now = datetime.now()
    context = {
        'events': events,
        'tag': tag,
        'time_now': time_now,
        'date_now':date_now,
        'no_events':no_events,
        'page':page,
        'city':city,
        'monthday': monthday,
        'day': day,
    }
    if weekday:
        print(weekday)
        context['events'] = events.filter(start_date__week_day=int(weekday)+1)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        context['events'] = events.filter(tags__in=[tag])
        no_events = events.count()
    if city:
        context['events'] = events.filter(city=city)
        no_events = events.count()
    if day:
        context['events'] = events.filter(start_date__icontains=day)
        no_events = events.count()
    if this_week:
        time_now = timezone.now()
        in_7_days = time_now + timedelta(days=7)
        context['events'] = events.filter(start_date__range=(time_now, in_7_days))
        no_events = events.count()
    if by_month:
        time_now = timezone.now()
        in_30_days = time_now + timedelta(days=30)
        context['events'] = events.filter(start_date__range=(time_now, in_30_days))
        no_events = events.count()
    if monthday:
        context['events'] = events.filter(start_date__week_day=weekdays[monthday.lower()])
        no_events = events.count()
    if request.method == 'POST':
        location = request.POST.get('location_search')
        start_date = request.POST.get('date_search')
        weekday = request.POST.get('weekday_search')
        rating = request.POST.get('rating')
        event_sort_by = request.POST.get('sort_by')
        if location:
            context['location'] = location
            context['events'] = Event.objects.filter(city__icontains=location)
        if weekday:
            for key in weekdays.keys():
                if weekday in key:
                    result = key
                    context['weekday'] = result
                    context['events'] = Event.objects.filter(start_date__week_day=weekdays[result])
        if start_date:
            context['events'] = Event.objects.filter(start_date__date=start_date)
        if location and start_date:
            context['events'] = Event.objects.filter(city__icontains=location, start_date__date=start_date)
        if event_sort_by:
            if event_sort_by == 'event_date_asc':
                context['events'] = Event.objects.all().order_by('created_on')
            if event_sort_by == 'event_date_des':
                context['events'] = Event.objects.all().order_by('-created_on')
            if event_sort_by == 'event_rate_asc':
                context['events'] = Event.objects.all().order_by('created_on')
            if event_sort_by == 'event_rate_des':
                context['events'] = Event.objects.all().order_by('created_on')
            if event_sort_by == 'event_start_asc':
                context['events'] = Event.objects.all().order_by('start_date')
            if event_sort_by == 'event_start_des':
                context['events'] = Event.objects.all().order_by('-start_date')

        if rating:
            if rating == '5':
                context['events'] = Event.objects.annotate(avg_rating=Avg('event_ratings__rate')).filter(avg_rating__gte=5)
            if rating == '4':
                context['events'] = Event.objects.annotate(avg_rating=Avg('event_ratings__rate')).filter(avg_rating__gte=4)
            if rating == '3':
                context['events'] = Event.objects.annotate(avg_rating=Avg('event_ratings__rate')).filter(avg_rating__gte=3)

   
    return render(request, templateFileName, context)


def event_details(request, pk):
    templateFileName = 'mainapp/events/eventDetails.html'
    page = 'event_details'
    event = Event.published.get(id=pk)
    src = f"https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d2128.1919194050733!2d{str(event.longitude)}!3d{str(event.latitude)}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m2!1m1!2zNTTCsDEwJzUyLjciTiAxNcKwMzQnMjcuOSJF!5e1!3m2!1spl!2spl!4v1741851245110!5m2!1spl!2spl"
    event_tags_ids = event.tags.values_list('id', flat=True)
    similar_posts = Event.published.filter(tags__in=event_tags_ids).exclude(id=event.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    time_now = datetime.now()
    ratings = Rating.objects.filter(event=event)
    news = News.objects.filter(event=event)


    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        news_form = NewsForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.event = Event.published.get(id=pk)
            new_comment.save()
        if news_form.is_valid():
            cd = news_form.cleaned_data
            News.objects.create(user=request.user, event=event, title=cd['title'], body=cd['body'])
    else:
        comment_form = CommentForm()
        news_form = NewsForm()

    comments = event.event_comments.all().order_by('-created_on')
    context = {
            'event': event,
            'src': src,
            'similar_posts':similar_posts,
            'time_now': time_now,
            'comment_form': comment_form,
            'comments':comments,
            'ratings':ratings,
            'page': page,
            'news': news,
            'news_form': news_form,
        }
    if request.user.is_authenticated:
        if Followed.objects.filter(user=request.user, event=event).exists():
            context['obserwuje'] = True
        else:
            context['obserwuje'] = False

    return render(request, templateFileName, context)


def event_ratings(request, event):
    templateFileName = 'mainapp/events/event_ratings.html'
    event = Event.objects.get(id=event)
    ratings = Rating.objects.filter(event=event).order_by('-rating_date')
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            cd = rating_form.cleaned_data
            Rating.objects.create(user=request.user, event=event,
                                  rate=cd['rate'], body=cd['body'] )
    else:
        rating_form = RatingForm()
    context = {
            'event': event,
            'ratings': ratings,
            'rating_form': rating_form,
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
    attraction = Attraction.objects.get(id=pk)
    context = {
        'attraction':attraction,
    }
    return render(request, templateFileName, context)


@login_required
def addEvent(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            cd = event_form.cleaned_data
            my_tags = cd['tags']
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.status = 'PB'
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
def editEvent(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event_form = EventForm(instance=event,
                               data=request.POST,
                               files=request.FILES)
        if event_form.is_valid():
            event_form.save()
            return redirect('account:dashboard')

    else:
        event_form = EventForm(instance=event)
    return render(request, 'mainapp/events/event_form.html', {'event_form': event_form})


@login_required
def del_event(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('account:dashboard')
    context = {
        'event':event,
    }
    return render(request, 'mainapp/events/del_event.html', context)

@login_required
def del_attraction(request, pk):
    attraction = Attraction.objects.get(id=pk)
    if request.method == 'POST':
        attraction.delete()
        return redirect('account:dashboard')
    context = {
        'attraction':attraction,
    }
    return render(request, 'mainapp/attractions/del_attraction.html', context)

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


@login_required
def editAttraction(request, pk):
    attraction = Attraction.objects.get(id=pk)
    if request.method == 'POST':
        attraction_form = AttractionForm(data=request.POST,
                                         instance=attraction,
                                         files=request.FILES)
        if attraction_form.is_valid():
            attraction_form.save()
            return redirect('account:dashboard')
    else:
        attraction_form = AttractionForm(instance=attraction)
    context = {
        'attraction_form':attraction_form,
    }
    return render(request, 'mainapp/attractions/attraction_form.html', context)


@login_required
def follow_event(request, pk, page=None):
    event = Event.published.get(id=pk)
    user = request.user

    if Followed.objects.filter(user=user, event=event).exists():
        pass
    else:
        Followed.objects.create(user=user, event=event)
    if page == 'events':
        return redirect('mainapp:events')
    elif page == 'home':
        return redirect('mainapp:home')
    elif page == 'event_details':
        return redirect('account:dashboard')



@login_required
def unfollow_event(request, pk, page=None):
    user_follow = Followed.objects.get(event=pk,
                                       user=request.user)
    user_follow.delete()
    event = Event.objects.get(id=pk)
    if page == 'eventDetails':
        return redirect(event.get_absolute_url())
    elif page == 'dashboard':
        return redirect('account:dashboard', option='follows')
    elif page == 'events':
        return redirect('mainapp:events')
    elif page == 'home':
        return redirect('mainapp:home')