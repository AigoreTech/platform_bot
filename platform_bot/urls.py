# platform_bot/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.authentication.urls')),  # Menyertakan URL aplikasi authentication
    path('', include('apps.dashboard.urls')),  # Menyertakan URL aplikasi dashboard
    path('', include('apps.users.urls')),  # Menyertakan URL aplikasi users
    path('', include('apps.bots.urls')),  # Menyertakan URL aplikasi bots
    path('', include('apps.webhook.urls')),  # Menyertakan URL aplikasi webhook
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
