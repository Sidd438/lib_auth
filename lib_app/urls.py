from django.urls import path, include
from lib_app.views import home, book_profile, issue

urlpatterns = [
    path('accounts/profile/', home),
    path('book', book_profile),
    path('Issue', issue)
]
