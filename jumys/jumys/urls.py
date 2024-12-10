from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.views.generic import RedirectView
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include API endpoints
    path('api/users/', include('users.urls')),
    path('api/seekers/', include('seekers.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/vacancies/', include('vacancies.urls')),
    path('api/follows/', include('follows.urls')),
    path('api/analytics/', include('analytics.urls')),

    # Home page
    path('home/', home_view, name='home'),

    # OpenAPI Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Generates the OpenAPI schema
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc UI

    # If you want to redirect root to Swagger UI (optional)
    path('', RedirectView.as_view(pattern_name='swagger-ui', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
