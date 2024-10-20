from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('login/', views.user_login, name='login'),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_registration, name="registration"),
    path("user-delete/", views.user_delete, name="user-delete"),

]
