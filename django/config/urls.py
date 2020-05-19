from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.generic import TemplateView

from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache

sitemaps = {
    'posts': PostSitemap,
}

handler404 = 'blog.views.page_not_found'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('summernote/', include('django_summernote.urls')),
    path('', include('blog.urls')),
    path('', include('comments.urls')),
    path('sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
