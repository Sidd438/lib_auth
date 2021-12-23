
from django.urls import path
from librarian.views import logging, logina, logoutA, profile



urlpatterns = [
    path('librarian/', logina),
    path('librarian/liblog/', logging),
    path('librarian/liblog/profile', profile),
    path('logoutlib', logoutA)
]

