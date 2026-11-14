from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['landing:index', 'landing:nosotros', 'landing:productos', 'landing:calidad', 'landing:cotizador']

    def location(self, item):
        return reverse(item)


def robots_txt(request):
    body = chr(10).join([
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /cotizacion/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
        "",
    ])
    return HttpResponse(body, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': {'pages': StaticPagesSitemap}}, name='sitemap'),
    path('', include('landing.urls', namespace='landing')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
