from allauth.account.forms import SignupForm
from django import forms
from .models import Rating



class UploadFileForm(forms.Form):
    file = forms.FileField()


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = {'rating'}
