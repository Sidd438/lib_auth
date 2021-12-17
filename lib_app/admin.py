from django.contrib import admin
from lib_app.models import Book, Issue, Denied, Issued
# Register your models here.
admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(Denied)
admin.site.register(Issued)
