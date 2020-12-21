from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from django_crm import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include(('auth_path.urls', 'auth_path'), namespace='auth_path')),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('user/', include(('user_profile.urls', 'user'), namespace='user')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
