from django.shortcuts import render
from .models import Event, Category
from django.core.paginator import Paginator

def home(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(events, 4)
    page_number = request.GET.get('page', 1)
    events = paginator.page(page_number)

    context = {
        'events': events,
        'categories': categories,
    }
    return render(request, 'main/main.html', context)

def eventView(request, pk):

    event = Event.objects.get(id=pk)
    categories = event.categories.all()
    context = {
        'event': event,
        'categories': categories,
    }
    return render(request, 'main/event-view.html', context)

def categoryList(request, cat):

    category = Category.objects.get(name=cat)
    events = Event.objects.filter(categories = category)

    context = {
        'category': category,
        'events': events,

    }
    return render(request, 'main/category-list.html', context)