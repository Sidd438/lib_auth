
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from admina.views import logoutA

urlpatterns = [
    path('super/', admin.site.urls),
    path('admin/', include('admina.urls')),
    path('', include('lib_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('librarian.urls')),
    path('api/', include('api.urls')),
    path('admlogout',logoutA),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
