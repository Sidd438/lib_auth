from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bits_id = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=20,null=True)
    room_no = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=12, null=True)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
