from django import forms
from .models import Rating
from django.core.validators import FileExtensionValidator



class UploadFileForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = {'rating'}

class ProfileForm(forms.Form):
    bits_id = forms.CharField(max_length=12, min_length=12)
    hostel = forms.CharField(max_length=50)
    room = forms.IntegerField(max_value=999, min_value=1)
    phone_number = forms.IntegerField()