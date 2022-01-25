from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import (BookList, BookDetail,
                 mixinsList, MixinDetail, BookViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('book_route', BookViewSet)

urlpatterns = [
    path('book/', BookList.as_view()),
    path('book/<int:isbn>/', BookDetail.as_view()),
    path('mixins/',mixinsList.as_view()),
    path('mixins/<int:pk>/', MixinDetail.as_view()),
    path('', include(router.urls))
]
