from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Profile
from django.db.models import Count
from mainapp.models import Followed, User, Event, Attraction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required

# def user_login(request):
#     templateFileName = 'account/login.html'
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('authentication completed successfully')
#                 else:
#                     return HttpResponse('account is disabled')
#             else:
#                 return HttpResponse('non correct authentication data')
#     else:
#         form = LoginForm()
        
#     context = {
#         'form': form,
#     }
#     return render(request, templateFileName, context)


@login_required
def dashboard(request, option='events'):
    templateFileName = 'account/dashboard.html'
    profile = get_object_or_404(Profile,
                                user = request.user.id)
    user = request.user
    events = Event.objects.filter(created_by=request.user)
    # event_follows = events.annotate(follow_number=Count('name'))
    # profile = Profile.objects.get(user = request.user.id)
    followed = Followed.objects.filter(user=request.user).annotate(follow_number=Count('event'))
    attractions = Attraction.objects.filter(created_by=request.user)

    option_page = None

    if option == 'events':
        option_page = 'account_events'

    if option == 'follows':
        option_page = 'account_follows'

    if option == 'attractions':
        option_page = 'account_attractions'

    page = 'account'

    context = {
        'profile': profile,
        'user': user,
        'followed': followed,
        'attractions':attractions,
        'events':events,
        'page': page,
        'option_page': option_page,
    }

    return render(request, templateFileName, context)


@login_required
def messages(request):

    context = {

    }
    return render(request, 'account/messages.html', context)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # creating a profile for new user
            Profile.objects.create(user=new_user)
            return render(request, 'account/register.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')
