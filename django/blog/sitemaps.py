from .models import Post
from django.contrib.sitemaps import Sitemap


class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.all().order_by('id')

    def lastmod(self, obj):
        return obj.created


