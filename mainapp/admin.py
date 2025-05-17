from django.contrib import admin
from .models import Event, Attraction, Comment, Followed, Rating
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_by', 'publish', 'status']
    list_filter = ['status', 'created_by', 'publish']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['created_by']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_by', 'publish', 'status']
    list_filter = ['status', 'created_by', 'publish']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['created_by']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_on']

@admin.register(Followed)
class FollowedAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'follow_date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'rate', 'rating_date']