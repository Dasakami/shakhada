from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView



urlpatterns = [
    path('', views.home, name='home' ),
    path('work/', views.work, name='work' ),
    path('faq/', views.faq, name='faq' ),
    path('how_it_works/', views.how_it_works, name='how_it_works' ),
    path('yandex_20c50dbebd35d885.html', views.yandex, name='yandex_20c50dbebd35d885.html' ),
    path('users/', include('users.urls', namespace='users')),
    path('request/', include('request.urls', namespace='request')),
    path('open-admin/', views.open_admin, name='admin'),
    path('notifications/', include('notifications.urls', namespace='notifications'))
]
