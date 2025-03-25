from django.urls import path
from . import views



app_name = 'mainapp' # better to use app_name in app urls.py !!!!!!!!!!!!!!
#django.core.exceptions.ImproperlyConfigured: Specifying a namespace in include()
# without providing an app_name is not supported. Set the app_name attribute in the included module,
#  or pass a 2-tuple containing the list of patterns and app_name instead.
urlpatterns = [
    path('', views.home, name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('events/', views.events, name='events'),
    path('tag/<slug:tag_slug>/', views.events, name='events_by_tag'),

    path('event/<int:pk>', views.event_details, name='event_details'),
    path('events/new-event/', views.addEvent, name='add_event'),
    path('attractions/', views.attractions, name='attractions'),
    path('attraction/<int:pk>', views.attraction_details, name='attraction_details'),

]
