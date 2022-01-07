from django.contrib import admin
from lib_app.models import Book, Issue, Profile, Rating, Renew, Review, Spreadsheet

admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Renew)
admin.site.register(Spreadsheet)
admin.site.register(Rating)