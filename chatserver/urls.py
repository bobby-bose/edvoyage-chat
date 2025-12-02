from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatapp.urls')),
    path('', include('chatapp.frontend_urls')),
]

# Serve media files in both DEBUG and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
