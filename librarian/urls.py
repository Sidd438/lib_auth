from django.contrib.auth import logout
from django.urls import path, include
from librarian.views import logging, login, logoutA
from django.conf.urls.static import static


urlpatterns = [
    path('librarian/', login),
    path('librarian/liblog/', logging),
    path('logoutlib', logoutA)
]

