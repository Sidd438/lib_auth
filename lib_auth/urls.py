
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lib_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('librarian.urls'))
]
