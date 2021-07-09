from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request,'Books/index.html')


def about(request):
    return render(request,'Books/about.html')







