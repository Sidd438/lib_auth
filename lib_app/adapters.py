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


