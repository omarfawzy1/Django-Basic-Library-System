import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Book, Booking


# Create your views here.


def bookInfo(request):
    print(Book.objects.all())
    print(Book.objects.values('{cat}').distinct())
    return render(request, 'Books/BooksBrowser.html',
                  {'books': Book.objects.all(), 'cats': Book.objects.values('{cat}').all()})


@login_required
def book(request, bookID):
    book = Book.objects.get(id=bookID)
    if Booking.objects.filter(book=book).exclude(user=request.user).exists():
        return HttpResponse("This Book is Not Avaliable Right Now")

    return render(request, 'BookInfo.html', {'book': book, 'booking': Booking.objects.filter(book=book)})


def search(request):
    if not request.user.is_authenticated:
        return redirect('signIn')
    books = Book.objects.exclude(id__in=Booking.objects.values_list('book'))
    cats = Book.objects.values('cat').distinct()
    bbooks = Book.objects.filter(id__in=Booking.objects.filter(user=request.user).values_list('book'))
    fileds = ['Title', 'ISBN', 'Author', 'Publish Date']
    if request.GET:
        searchBy = request.GET['searchBy']
        if searchBy in fileds:
            value = request.GET['searchValue']
            if searchBy == 'Title':
                books = Book.objects.filter(title__contains=value)
            elif searchBy == 'ISBN':
                books = Book.objects.filter(ISBN__icontains=value)
            elif searchBy == 'Author':
                books = Book.objects.filter(authorName__icontains=value)
            else:
                books = Book.objects.filter(publishDate=value)

        elif request.GET['searchValue'] != '':
            books = Book.objects.filter(title__contains=request.GET['searchValue'])
            print('by title')

        print("Books Are Ready")
        print(books.count)

        return render(request, 'bookInformation.html', {'books': books, 'cat': cats, 'fileds': fileds})
    return render(request, 'HomePage.html', {'books': books, 'cat': cats, 'fileds': fileds, 'borrowedBooks': bbooks})


# Return a Page of Books Based on Search Values.
@login_required
def searchAjax(request, searchValue=None, searchBy='Title'):
    fileds = ['Title', 'ISBN', 'Author', 'Publish Date']
    books = Book.objects.all()
    if (searchValue == '' or searchValue == None):
        return render(request, 'Book.html', {'books': books})

    if (searchBy in fileds):
        if (searchBy == 'Title'):
            books = Book.objects.filter(title__contains=searchValue)
        elif (searchBy == 'ISBN'):
            books = Book.objects.filter(ISBN__icontains=searchValue)
        elif (searchBy == 'Author'):
            books = Book.objects.filter(authorName__icontains=searchValue)
        else:
            searchValue = datetime.datetime.strptime(searchValue, "%Y-%m-%d").date()
            books = Book.objects.filter(publishDate=searchValue)
            if (not books):
                books = Book.objects.filter(publishDate__year=searchValue.year)

    elif searchValue != '':
        books = Book.objects.filter(title__contains=searchValue)

    return render(request, 'Book.html', {'books': books})


@login_required
def filterCategory(request, category):
    books = Book.objects.filter(cat__contains=category)
    return render(request, 'Book.html', {'books': books})


def signIn(request):
    if request.user.is_authenticated:
        return redirect('search')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('search')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    return render(request, 'SignIn.html')


def user_logout(request):
    logout(request)
    return redirect('signIn')


def orderDate(request): return render(request, 'book.html', {'book': Book.objects.order_by('publishDate')})


def signUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).first():
            return HttpResponse("username already taken")
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.is_staff = (request.POST.get('isAdmin') == 'on')
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('search')
            else:
                return HttpResponse("Your account was inactive.")
        return HttpResponse("failed")
    return render(request, 'SignUp.html')


def addBook(request):
    if (request.method == "POST"):
        isbn = request.POST.get("ISBN")
        if (Book.objects.filter(ISBN=isbn).first()):
            return HttpResponse("A Book with the same ISBN already exists")
        book = Book.objects.create(ISBN=isbn)
        book.title = request.POST.get("title")
        book.authorName = request.POST.get("authorName")
        book.publishDate = request.POST.get("publishDate")
        book.cat = request.POST.get("category")
        book.descritption = request.POST.get("descritption")
        book.summary = request.POST.get("summary")
        myfile = request.FILES['cover']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        book.cover = myfile
        book.save()
    return render(request, 'addBook.html', )


def userinfo(request):
    if request.method == 'POST':
        user = request.user
        if (user.username != request.POST.get('username')):
            nusername = request.POST.get('username')
            if User.objects.filter(username=nusername).first():
                return HttpResponse("username already taken")
            else:
                user.username = nusername
                user.save()

        if (user.first_name != request.POST.get('fname')):
            fname = request.POST.get('fname')
            user.first_name = fname
            user.save()

        if (user.last_name != request.POST.get('lname')):
            lname = request.POST.get('lname')
            user.last_name = lname
            user.save()

        if (user.email != request.POST.get('email')):
            email = request.POST.get('email')
            user.email = email
            user.save()

        if (request.POST.get('password') != ''):
            password = request.POST.get('password')
            user.set_password(password)
            user.save()

    return render(request, 'userInfo.html', )


def borrow(request, id):
    if (request.method == 'GET'):
        book = Book.objects.get(id=id)
        user = request.user
        today = datetime.datetime.today() + datetime.timedelta(days=3)
        try:
            booking = Booking.objects.create(user=user, book=book, returnDate=today)
            booking.save()
            return HttpResponse(("Successfully ", booking.returnDate.strftime("%m/%d/%Y")))
        except:
            return ("Failed")


def returnBook(request, id):
    if (request.method == 'GET'):
        book = Book.objects.get(id=id)
        user = request.user
        try:
            booking = Booking.objects.filter(book=book, user=user).first()
            booking.delete()
            return HttpResponse("Successfully returned Book")
        except:
            return HttpResponse("Booking not Found")


def extend(request, id):
    if (request.method == 'GET'):
        book = Book.objects.get(id=id)
        user = request.user

        try:
            booking = Booking.objects.filter(book=book, user=user).first()
            date = booking.returnDate

            differnce = (date.date() - datetime.datetime.today().date()).days
            print(differnce)
            if (differnce < 4):
                date = date + datetime.timedelta(days=3)
                booking.returnDate = date
                # booking.save()
            else:
                return HttpResponse("can't extend time")

            return HttpResponse(("Successfully ", booking.returnDate.strftime("%m/%d/%Y")))
        except:
            return HttpResponse("Failed")
