from django.urls import path, include
from lib_app.views import home, book_data, issue

urlpatterns = [
    path('accounts/profile/', home),
    path('book', book_data),
    path('Issue', issue)
]
