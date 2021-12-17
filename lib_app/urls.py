from django.urls import path, include
from lib_app.views import home, book_profile, issue
from lib_app.views import profile

urlpatterns = [
    path('accounts/profile/', home),
    path('book', book_profile),
    path('Issue', issue),
    path('accounts/profile/profile', profile)
]
