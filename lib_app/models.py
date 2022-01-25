from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Spreadsheet(models.Model):
    file = models.FileField(upload_to='spreadsheets')


class Book(models.Model):
    image_link = models.TextField(
        null=True)
    name = models.CharField(max_length=100)
    summary = models.TextField()
    author = models.CharField(max_length=30, null=True)
    genre = models.CharField(max_length=30, null=True)
    isbn = models.IntegerField(null=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, default= 'ask the librarian')
    issues = models.IntegerField(default=0)
    brating = models.FloatField(default=5)
    bratings = models.IntegerField(default=0)

    def __str__(self):
        return (self.name)


class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField()
    pending = models.BooleanField(default=True)
    issued = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    reason = models.TextField(null=True)
    returned = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    due_date = models.DateField(null=True)

    def __str__(self):
        return (self.book.name +" "+ self.user.username) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bits_id = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=20, null=True)
    room_no = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
    merit = models.FloatField(default=100)
    returns = models.IntegerField(default=0)
    
    def __str__(self):
        return (self.user.username)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.book.name+" "+self.user.username)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return (self.book.name)

class Renew(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    time = models.IntegerField()

    def __str__(self):
        return (self.issue.book.name+" "+self.issue.user.username)
