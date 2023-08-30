from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter()

admin.site.site_title = 'CES'
admin.site.site_header = 'CES'
admin.site.index_title = 'CES ADMIN'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
