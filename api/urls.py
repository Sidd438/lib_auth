from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import (BookList, BookDetail, IssueViewSet, logoutapi, IssueDetail, IssueList,
                 mixinsList, MixinDetail, BookViewSet, regestration_func)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router1 = DefaultRouter()
router1.register('book_route', BookViewSet)
router1.register('issue_route', IssueViewSet)

urlpatterns = [
    path('book/', BookList.as_view()),
    path('book/<int:isbn>/', BookDetail.as_view()),
    path('mixins/',mixinsList.as_view()),
    path('mixins/<int:pk>/', MixinDetail.as_view()),
    path('issue/', IssueList.as_view()),
    path('issue/<int:pk>/', IssueDetail.as_view()),
    path('', include(router1.urls)),
    path('login/', obtain_auth_token, name='Token_Login'),
    path('registration/', regestration_func, name='Token_Registration'),
    path('logout/', logoutapi),
    path('api-auth/', include('rest_framework.urls')),

]
