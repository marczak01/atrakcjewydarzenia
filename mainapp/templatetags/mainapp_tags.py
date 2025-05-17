from urllib import request
from django.db.models import Avg
from django import template
from ..models import Event, Attraction, Followed, Rating
from datetime import date, datetime, timedelta

register = template.Library()

# custom tag created for calculating no "days to event"
@register.simple_tag
def substract(a, b):
    return int(a) - int(b)

@register.simple_tag
def multiply(a, b):
    return int(a) * int(b)


@register.simple_tag
def add(a, b):
    return int(a) + int(b)

@register.simple_tag
def add_date(a, b):
    return a + timedelta(days=b)

@register.simple_tag
def absolute(a):
    return abs(a)

@register.simple_tag
def no_days(a, b, c, d):
    a =int(a)
    b =int(b)
    c=int(c)
    d=int(d)
    if c - d > 0:
        years_diff = (c - d) * 365
        days_diff = years_diff + abs(a-b)
        return days_diff
    elif c - d <= 0:
        days_diff = a-b
        return days_diff



@register.simple_tag
def follow_count(event):
    return Followed.objects.filter(event=event).count()

@register.simple_tag
def follow_or_unfollow(event, user):
    obserwuje = None
    if Followed.objects.filter(event=event, user=user).exists():
        obserwuje = True
        return obserwuje
    else:
        obserwuje = False
        return obserwuje


@register.simple_tag
def count_rating_event(event):
    rating_sum = 0
    event = Event.objects.get(id=event.id)
    ratings = Rating.objects.filter(event=event)
    for rating in ratings:
        rating_sum += rating.rate
    if ratings.count() == 0:
        rating_result = 'brak ocen'
        return rating_result
    else:
        rating_result = rating_sum / ratings.count()
        return rating_result
    
@register.simple_tag
def count_ratings(event):
    event = Event.objects.get(id=event.id)
    ratings = Rating.objects.filter(event=event)
    return ratings.count()
# @register.simple_tag
# def search_form(option):
#     weekdays = {'poniedziałek' : 1,
#                 'poniedzialek': 1,
#                 'wtorek': 2,
#                 'sroda': 3,
#                 'środa': 3,
#                 'czwartek': 4,
#                 'piatek': 5,
#                 'piątek': 5,
#                 'sobota': 6,
#                 'niedziela': 7}

#     if option in weekdays:
#         events = Event.objects.filter(start_date__week_day=weekdays[option])
#     return events
