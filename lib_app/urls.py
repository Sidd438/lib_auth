from django.urls import path
from lib_app.views import home, book_profile, profile, logoutA, editprofile, red, similar

urlpatterns = [
    path('accounts/profile/', home),
    path('book', book_profile),
    path('accounts/profile/profile', profile),
    path('accounts/profile/editor', editprofile),
    path('accounts/signup/', red),
    path('logout', logoutA),
    path('', red),
    path('similar',similar)
    
]
