from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from .views import LoginView, LogoutView

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^logout/$', LogoutView.as_view(), name='logout'),
        url(r'^login/$', LoginView.as_view(), name='login'),
        url(r'^', include('grid.urls')),
        ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
