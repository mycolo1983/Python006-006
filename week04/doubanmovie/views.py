from django.shortcuts import render
from .models import MovieTest

# Create your views here.

def index(request):
    return render(request,'index.html')


def searchMovie(request):
    if request.method == 'POST':
        moviename = request.POST.get('q')
    n = MovieTest.objects.filter(name=moviename,stars__gt='3')
    return render(request,'search.html',locals())
