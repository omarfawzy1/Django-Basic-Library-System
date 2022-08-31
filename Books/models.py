from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, EmailField, IntegerField
from django.contrib.auth.models import User
import datetime


class Book(Model):
    ISBN = CharField(max_length=100, unique=True, default=False)
    title = CharField(max_length=100)
    authorName = CharField(max_length=100)
    cover = models.ImageField(upload_to='covers', default="")
    isBooked = BooleanField(default=False)
    summary = models.TextField(default="Book Summary", help_text="Enter Book Summary")
    description = models.TextField(default="Book Description")
    publishDate = models.DateField(default=datetime.date.today)
    cat = CharField(max_length=120, default='')

    def __str__(self):
        return self.title


class Booking(Model):
    user = models.ForeignKey(User, on_delete=CASCADE, default='null')
    book = models.ForeignKey(Book, on_delete=CASCADE, default='null')
    returnDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.book)
    # Create your models here.
