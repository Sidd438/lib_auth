from django import forms
from .models import Rating
from django.core.validators import FileExtensionValidator, RegexValidator



class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = {'rating'}

class ProfileForm(forms.Form):
    bits_id = forms.CharField(max_length=13, min_length=13, validators=[RegexValidator(regex=r"\d\d\d\d\D\d\D\D\d\d\d\d\D", message="Invalid BITS-ID")])
    hostel = forms.CharField(max_length=50, validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$')])
    room = forms.IntegerField(max_value=999, min_value=1)
    phone_number = forms.IntegerField(max_value=9999999999, min_value=1000000000)
    