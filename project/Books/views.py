from django.shortcuts import render
from .models import Book
# Create your views here.

def index(request):
    return render(request,'Books/index.html')


def about(request):
    return render(request,'Books/about.html')

def bookInfo(request):
    return render(request,'Books/BooksBrowser.html',{'books' : Book.objects.all()})







