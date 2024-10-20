from django.shortcuts import render

# Create your views here.
def blogView(request):
    context = {

    }
    return render(request, 'blog/blog.html', context)