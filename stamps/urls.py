from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from mainapp.sitemap import StampGroupSitemap, StampSitemap
from printy.sitemap import PrintyGroupSitemap, PrintySitemap

sitemaps = {
    "StampsGroups": StampGroupSitemap,
    "Stamps": StampSitemap,
    "PrintyGroup": PrintyGroupSitemap,
    "Printy": PrintySitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "ckeditor5/",
        include("django_ckeditor_5.urls"),
        name="ck_editor_5_upload_file",
    ),
    path("about/", include("about.urls", namespace="about")),
    path("admin/", admin.site.urls),
    path("printy/", include("printy.urls", namespace="printy")),
    path("", include("mainapp.urls", namespace="mainapp")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
