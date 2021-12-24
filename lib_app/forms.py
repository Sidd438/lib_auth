from django import forms
from .models import Rating
from django.core.validators import FileExtensionValidator



class UploadFileForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['xlsv'])])


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = {'rating'}
