from django.db import models
from django.db.models.fields import CharField



class Book (models.Model):
        title = CharField(max_length=100, default="")
        authorName = CharField(max_length=100)
        cover = models.ImageField(upload_to = 'covers', default="")

# Create your models here.
