from django.urls import path, include
from librarian.views import logging, login

urlpatterns = [
    path(r'librarian/', login),
    path(r'librarian/liblog/', logging),
]
