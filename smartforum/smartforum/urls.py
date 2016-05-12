from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from forum import views
from . import settings

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    url(r'^forum/', include('forum.urls')),
	url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
