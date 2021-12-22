
from django.urls import path
from librarian.views import logging, login, logoutA



urlpatterns = [
    path('librarian/', login),
    path('librarian/liblog/', logging),
    path('logoutlib', logoutA)
]

