from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # обязательно
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('auth/', include('authorization.urls')),
    path('', include('dashboard.urls')),
    path('blood/', include('blood.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
