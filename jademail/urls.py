from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        # url(r'^', auth_views.login, name='login'),
        url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
        url(r'^test/', include('grid.urls')),
        ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
