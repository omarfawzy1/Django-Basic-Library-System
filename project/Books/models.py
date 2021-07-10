from django.db import models
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, EmailField
import datetime


class User(Model):

    name = CharField(max_length=100)
    email = EmailField()

    def __str__(self):
        return self.name


class Book (Model):

    title = CharField(max_length=100)
    authorName = CharField(max_length=100)
    cover = models.ImageField(upload_to='covers', default="")
    isBooked = BooleanField(default=False)
    summary = models.TextField(default="Book Summary", help_text="Enter Book Summary")
    description = models.TextField(default="Book Description")
    publishDate = models.DateField(default=datetime.date.today)
    borrower = models.ForeignKey(User, on_delete=CASCADE, default='null')
    returnDate = models.DateTimeField(null=True, blank=True)
    returnReson = models.CharField(max_length=150, blank=True)
    cat = CharField(max_length=120,default='')

    def __str__(self):
        return self.title
# Create your models here.
