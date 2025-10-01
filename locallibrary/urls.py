from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView  # Required for your root redirect
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # 1. Admin site URL
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), #serve media files when deployed
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), #serve static files when deployed

    # 2. Registration App URLs (e.g., /register/signup/)
    path('register/', include('register.urls')),

    # 3. Catalog app URLs
    path('catalog/', include('catalog.urls')),

    # 4. Redirect the base URL (e.g., mysite.com/) to /catalog/
    path('', RedirectView.as_view(url='catalog/', permanent=True)),

    # 5. Built-in Authentication URLs (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Removed the duplicate 'path('', include('register.urls')),' which was conflicting.
]+ static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)


# Add URL patterns to serve static and media files ONLY when in development (DEBUG mode).
# This is the correct and standard way to serve these files locally.
if settings.DEBUG:
    # 6. Serve static files (styles, scripts, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # 7. Serve media files (user-uploaded images)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
