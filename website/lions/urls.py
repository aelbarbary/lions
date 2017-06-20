from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'lions', include('lionsapp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.simple.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
