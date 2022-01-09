from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Libdata


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.groups.filter(name='Librarians').exists():
        if not Libdata.objects.filter(user=instance).exists():
            Libdata.objects.create(user=instance)
        
