from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User



class RestrictEmailAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if "@pilani.bits-pilani.ac.in" not in email:
            raise ValidationError('You are restricted from registering.\
                                            Please contact admin.')
        return email

class MyAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        try:
            user = User.objects.get(email=sociallogin.objects.get(user=request.user).extra_data.get('email'))
            sociallogin.connect(request, user)
            raise ImmediateHttpResponse('<h1>Wrong Domain</h1>')
        except User.DoesNotExist:
            pass
