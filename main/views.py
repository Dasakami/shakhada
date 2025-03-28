from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')

def work(request):
    return render(request, 'main/work.html')

def how_it_works(request):
    return render(request, 'main/how_it_works.html')
# Create your views here.
