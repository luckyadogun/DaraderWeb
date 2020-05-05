from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Darader Admin Portal"
admin.site.site_title = "Darader Admin Portal"
admin.site.index_title = "Welcome to Darader Admin Portal"

handler404 = "properties.views.handler404"

urlpatterns = [
    path('secret-saucer/', admin.site.urls),
    path('', include(('properties.urls', 'properties'), namespace='properties')),
    path('my/', include(('users.urls', 'users'), namespace='users')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
