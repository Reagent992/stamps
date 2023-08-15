from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('about/', include('about.urls', namespace='about')),
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls', namespace='mainapp')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
