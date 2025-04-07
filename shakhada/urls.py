from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from main.views import redirect_to_lang  # добавили

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'
handler403 = 'main.views.permission_denied'

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('suddenly/', admin.site.urls),
    *i18n_patterns(
        path('', include('main.urls')),
    ),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
