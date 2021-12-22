from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from lib_app.models import Profile
# Create your models here.


class Libdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    books_issued = models.IntegerField(default=0)
    books_added = models.IntegerField(default=0)
