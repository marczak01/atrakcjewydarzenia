
from django import template
from ..models import Event, Attraction

register = template.Library()

@register.simple_tag
def substract(a, b):
    return int(a) - int(b)