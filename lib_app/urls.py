from django.urls import path, include
from lib_app.views import home, book_profile, issue
from lib_app.views import profile,logoutA

urlpatterns = [
    path('accounts/profile/', home),
    path('book', book_profile),
    path('accounts/profile/profile', profile),
    path('logout', logoutA)
]
