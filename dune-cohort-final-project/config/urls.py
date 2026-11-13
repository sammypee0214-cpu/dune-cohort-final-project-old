"""Root URL configuration."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("inventory.api_urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("inventory.urls")),
    # Uploaded car photos. WhiteNoise only serves static files, so media is
    # served by Django. Note: Render's free disk is ephemeral, so uploads
    # disappear on redeploy (see README).
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
