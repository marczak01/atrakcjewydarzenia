from django.shortcuts import render

# Create your views here.
def eventsPage(request, *args, **kwargs):
    html_page = 'eventsPage.html'
    return render(request, html_page)
