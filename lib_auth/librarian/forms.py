from django import forms
from lib_app.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','image_link','summary','author','isbn','genre','location']