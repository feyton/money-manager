from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls',  namespace='rest_framework')),
    path('api/', include('finance.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
