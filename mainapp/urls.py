from django.urls import path
from . import views



app_name = 'mainapp' # better to use app_name in app urls.py !!!!!!!!!!!!!!
#django.core.exceptions.ImproperlyConfigured: Specifying a namespace in include()
# without providing an app_name is not supported. Set the app_name attribute in the included module,
#  or pass a 2-tuple containing the list of patterns and app_name instead.
urlpatterns = [
    path('', views.home, name='home'),
    path('welcome', views.welcome, name='welcome'),
    path('tag/<slug:tag_slug>/', views.events, name='events_by_tag'),
    path('events/', views.events, name='events'),
    path('events/add-event/', views.addEvent, name='add_event'),
    path('event/<int:pk>', views.event_details, name='event_details'),
    path('event/<int:pk>/followed', views.follow_event, name='follow_event'),
    path('attractions/', views.attractions, name='attractions'),
    path('attractions/add-attraction/', views.addAttraction, name='add_attraction'),
    path('attraction/<int:pk>', views.attraction_details, name='attraction_details'),

]
