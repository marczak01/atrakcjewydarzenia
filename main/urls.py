from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('event/<str:pk>/', views.eventView, name='event-view'),
    path('events/<str:cat>/', views.categoryList, name='category-list'),
]
