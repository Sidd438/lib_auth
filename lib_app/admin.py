from django.contrib import admin
from lib_app.models import Book, Issue, Denied, Issued, Profile

admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(Denied)
admin.site.register(Issued)
admin.site.register(Profile)
