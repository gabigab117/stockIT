from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from landing.views import index_view
from django.conf import settings

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', index_view, name="index"),
    path("account/", include("account.urls")),
    path("stockit/", include("stockit.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
