from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from mainapp.sitemap import StampGroupSitemap, StampSitemap
from printy.sitemap import PrintyGroupSitemap, PrintySitemap

sitemaps = {
    "StampsGroups": StampGroupSitemap,
    "Stamps": StampSitemap,
    "PrintyGroup": PrintyGroupSitemap,
    "Printy": PrintySitemap,
    "Pages": FlatPageSitemap,
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
    ),
    path("admin/", admin.site.urls),
    path("printy/", include("printy.urls", namespace="printy")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("", include("mainapp.urls", namespace="mainapp")),
    path("", include("orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
