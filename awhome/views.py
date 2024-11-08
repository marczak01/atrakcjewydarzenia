from django.shortcuts import render

def home(request, *args, **kwargs):
    html_page = 'homePage.html'
    return render(request, html_page)