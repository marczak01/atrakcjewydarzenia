
from django import template
from ..models import Event, Attraction

register = template.Library()

# custom tag created for calculating no "days to event"
@register.simple_tag
def substract(a, b):
    return int(a) - int(b)