from django.contrib.sitemaps import Sitemap

from mainapp.models import Stamp, StampGroup


class StampSitemap(Sitemap):
    """sitemap.xml для Печати."""

    changefreq = "monthly"

    def items(self):
        return Stamp.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated


class StampGroupSitemap(Sitemap):
    """sitemap.xml для Группы печатей."""

    changefreq = "monthly"

    def items(self):
        return StampGroup.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated
