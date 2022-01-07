from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.


class Libdata(models.Model):
    books_issued = models.IntegerField(default=0)
    books_added = models.IntegerField(default=0)
