from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


class Libdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    books_issued = models.IntegerField(default=0)
    books_added = models.IntegerField(default=0)

    
    def __str__(self):
        return (self.user.username)