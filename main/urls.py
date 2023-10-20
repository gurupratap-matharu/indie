from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from pages.sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("private/", admin.site.urls),
    # Set language
    path("i18n/", include("django.conf.urls.i18n")),
    # User management
    path("accounts/", include("allauth.urls")),
    path("account/", include("users.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("properties/", include("properties.urls")),
    path("portal/", include("portal.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("pages.urls")),
]


if settings.DEBUG:
    from django.views.generic import TemplateView

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add routes to test error templates
    urlpatterns += [
        path("test403/", TemplateView.as_view(template_name="403.html")),
        path("test404/", TemplateView.as_view(template_name="404.html")),
        path("test500/", TemplateView.as_view(template_name="500.html")),
    ]
