from django.contrib import admin
from django.urls import path

from .views import eventsPage

urlpatterns = [
    path('', eventsPage, name='events'),
]