from django.urls import path
from .views import logina, logging

urlpatterns = [
    path('', logina),
    path('adminlog/',logging)
]
