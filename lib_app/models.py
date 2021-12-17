from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import manager


class Book(models.Model):
    image_link = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=30)
    summary = models.TextField(max_length=100)
    author = models.CharField(max_length=30, null=True)
    genre = models.CharField(max_length=30, null=True)
    isbn = models.IntegerField(null=True)
    available = models.BooleanField(default=True)


class Issue(models.Model):
    username = models.CharField(max_length=35)
    book_id = models.IntegerField()
    time = models.IntegerField(default=7)
    book_name = models.CharField(max_length=30)


class Issued(models.Model):
    username = models.CharField(max_length=35)
    book_id = models.IntegerField()
    time = models.IntegerField(default=7)
    book_name = models.CharField(max_length=30)
    due_date = models.DateField(null=True)
    issue_date = models.DateField(auto_now=True)

class Denied(models.Model):
    username = models.CharField(max_length=35)
    book_id = models.IntegerField()
    reason = models.TextField()
    book_name = models.CharField(max_length=30)


'''class CustomUser(AbstractUser):
    bits_id = models.TextField(max_length=20)'''
