from django.contrib.auth import logout
from django.urls import path, include
from librarian.views import logging, login, logoutA

urlpatterns = [
    path(r'librarian/', login),
    path(r'librarian/liblog/', logging),
    path(r'logoutlib',logoutA)
]
