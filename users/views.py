from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def user_registration(request):
    # user registration view
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'],
                                            cd['user_email'],
                                            cd['password'])
            # log in after valid registration 
            # creating new_user variable for storing currently created
            # user and pass it into login() function to make him 
            # logged in after registration
            new_user = authenticate(username=cd['username'],
                                    password=cd['password'])
            login(request, new_user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context)


@login_required
def dashboard(request):
    # passing currently logged in user into template
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'users/dashboard.html', context)


def users(request):
    # rendering all users into template
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users/users.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('Authorization succeed!')
                    return redirect('dashboard')
                else:
                    return HttpResponse('Account is blocked.')
            else:
                return HttpResponse('Wrong authorization data.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def user_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')
    context = {

    }
    return render(request, 'registration/delete_form.html', context)