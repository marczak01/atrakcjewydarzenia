from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
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
def dashboard(request):
    templateFileName = 'account/dashboard.html'

    context = {

    }

    return render(request, templateFileName, context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            print('stworzone')
            return render(request, 'account/register.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})