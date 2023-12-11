from django.contrib.sitemaps import Sitemap

from printy.models import Printy, PrintyGroup


class PrintySitemap(Sitemap):
    """sitemap.xml для Печати."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Printy.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created


class PrintyGroupSitemap(Sitemap):
    """sitemap.xml для Группы печатей."""

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return PrintyGroup.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.created
