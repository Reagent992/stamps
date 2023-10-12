from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("about/", include("about.urls", namespace="about")),
    path("admin/", admin.site.urls),
    path("printy/", include("printy.urls", namespace="printy")),
    path("", include("mainapp.urls", namespace="mainapp")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
