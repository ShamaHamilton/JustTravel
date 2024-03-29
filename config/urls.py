"""justtravel URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jtadmin/', admin.site.urls),
    path('', include('blogs.urls')),
    path('account/', include('accounts.urls')),
    path('landlord/', include('landlord.urls')),
    path('rooms/', include('rooms.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)